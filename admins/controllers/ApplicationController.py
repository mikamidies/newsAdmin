from django.http import HttpRequest
from api.models import Application
from core.services import ModelViewService, ModelActionService
from core.router import BaseRouter
from django.shortcuts import render


application_router = BaseRouter("applications")

view_service = ModelViewService(
    model=Application, search_fields=["question", "answer"])
action_service = ModelActionService(model=Application,
                                    view_service=view_service,
                                    template_name="admin/application/form.html",
                                    redirect_to="/admin/applications")


@application_router.GET_request("/", name="application_list")
def list_view(request: HttpRequest):
    queryset = view_service.get_queryset_with_search(request)

    context = view_service.get_list_context_data(request, queryset)

    return render(request, "admin/application/list.html", context=context)


@application_router.GET_request("/<int:pk>/edit", name="application_edit")
def edit_get(request: HttpRequest, pk: int):
    instance = view_service.get_one(pk)

    if instance.new:
        instance.new = False
        instance.save()

    context = view_service.get_one_context_data(request, instance)

    return render(request, "admin/application/form.html", context=context)


@application_router.POST_request("/<int:pk>/edit", name="application_edit")
def edit_post(request: HttpRequest, pk: int):
    instance = view_service.get_one(pk)

    request_data = action_service.get_request_data(request)

    for key, value in request_data.items():
        setattr(instance, key, value)

    return action_service.save(request, instance)
