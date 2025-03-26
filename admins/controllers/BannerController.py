from django.http import HttpRequest
from api.models import Banner
from core.services import ModelViewService, ModelActionService
from core.router import BaseRouter
from django.shortcuts import redirect, render


banner_router = BaseRouter("banners")

view_service = ModelViewService(model=Banner, search_fields=["title"])
action_service = ModelActionService(model=Banner, view_service=view_service,
                                    image_fields=["image"],
                                    template_name="admin/banner/form.html",
                                    redirect_to="/admin/banners")


@banner_router.GET_request("/", name="banner_list")
def list_view(request: HttpRequest):
    queryset = view_service.get_queryset_with_search(request)

    context = view_service.get_list_context_data(request, queryset)

    return render(request, "admin/banner/list.html", context=context)


@banner_router.GET_request("/create", name="banner_create")
def create_get(request: HttpRequest):
    instance = Banner()

    action_service.predelete_image(request)

    context = view_service.get_one_context_data(request, instance)

    return render(request, "admin/banner/form.html", context=context)


@banner_router.POST_request("/create", name="banner_create")
def create_post(request: HttpRequest):
    request_data = action_service.get_request_data(request)

    instance = Banner(**request_data)

    return action_service.save(request, instance)


@banner_router.GET_request("/<int:pk>/edit", name="banner_edit")
def edit_get(request: HttpRequest, pk: int):
    instance = view_service.get_one(pk)

    action_service.predelete_image(request, str(pk))

    context = view_service.get_one_context_data(request, instance)

    return render(request, "admin/banner/form.html", context=context)


@banner_router.POST_request("/<int:pk>/edit", name="banner_edit")
def edit_post(request: HttpRequest, pk: int):
    instance = view_service.get_one(pk)

    request_data = action_service.get_request_data(request, pk)

    for key, value in request_data.items():
        setattr(instance, key, value)

    return action_service.save(request, instance)


@banner_router.POST_request("/<int:pk>/delete", name="banner_delete")
def delete(request: HttpRequest, pk: int):
    instance = view_service.get_one(pk)

    instance.delete()

    return redirect("/admin/banners")
