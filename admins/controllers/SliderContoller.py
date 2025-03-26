from django.http import HttpRequest
from api.models import Slider
from core.services import ModelViewService, ModelActionService
from core.router import BaseRouter
from django.shortcuts import redirect, render


slider_router = BaseRouter("sliders")

view_service = ModelViewService(model=Slider, search_fields=["title"])
action_service = ModelActionService(model=Slider, view_service=view_service,
                                    image_fields=["image"],
                                    template_name="admin/slider/form.html",
                                    redirect_to="/admin/sliders")


@slider_router.GET_request("/", name="slider_list")
def list_view(request: HttpRequest):
    queryset = view_service.get_queryset_with_search(request)

    context = view_service.get_list_context_data(request, queryset)

    return render(request, "admin/slider/list.html", context=context)


@slider_router.GET_request("/create", name="slider_create")
def create_get(request: HttpRequest):
    instance = Slider()

    action_service.predelete_image(request)

    context = view_service.get_one_context_data(request, instance)

    return render(request, "admin/slider/form.html", context=context)


@slider_router.POST_request("/create", name="slider_create")
def create_post(request: HttpRequest):
    request_data = action_service.get_request_data(request)

    instance = Slider(**request_data)

    return action_service.save(request, instance)


@slider_router.GET_request("/<int:pk>/edit", name="slider_edit")
def edit_get(request: HttpRequest, pk: int):
    instance = view_service.get_one(pk)

    action_service.predelete_image(request, str(pk))

    context = view_service.get_one_context_data(request, instance)

    return render(request, "admin/slider/form.html", context=context)


@slider_router.POST_request("/<int:pk>/edit", name="slider_edit")
def edit_post(request: HttpRequest, pk: int):
    instance = view_service.get_one(pk)

    request_data = action_service.get_request_data(request, pk)

    for key, value in request_data.items():
        setattr(instance, key, value)

    return action_service.save(request, instance)


@slider_router.POST_request("/<int:pk>/delete", name="slider_delete")
def delete(request: HttpRequest, pk: int):
    instance = view_service.get_one(pk)

    instance.delete()

    return redirect("/admin/sliders")
