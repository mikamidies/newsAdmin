from django.http import HttpRequest
from api.models import Videos
from core.services import ModelViewService, ModelActionService
from core.router import BaseRouter
from django.shortcuts import redirect, render


videos_router = BaseRouter("videos")

view_service = ModelViewService(model=Videos, search_fields=["title"])
action_service = ModelActionService(model=Videos, view_service=view_service,
                                 template_name="admin/videos/form.html",
                                 redirect_to="/admin/videos")


@videos_router.GET_request("/", name="videos_list")
def list_view(request: HttpRequest):
    queryset = view_service.get_queryset_with_search(request)
    context = view_service.get_list_context_data(request, queryset)
    return render(request, "admin/videos/list.html", context=context)


@videos_router.GET_request("/create", name="videos_create")
def create_get(request: HttpRequest):
    instance = Videos()
    context = view_service.get_one_context_data(request, instance)
    return render(request, "admin/videos/form.html", context=context)


@videos_router.POST_request("/create", name="videos_create")
def create_post(request: HttpRequest):
    request_data = action_service.get_request_data(request)
    instance = Videos(**request_data)
    return action_service.save(request, instance)


@videos_router.GET_request("/<int:pk>/edit", name="videos_edit")
def edit_get(request: HttpRequest, pk: int):
    instance = view_service.get_one(pk)
    context = view_service.get_one_context_data(request, instance)
    return render(request, "admin/videos/form.html", context=context)


@videos_router.POST_request("/<int:pk>/edit", name="videos_edit")
def edit_post(request: HttpRequest, pk: int):
    instance = view_service.get_one(pk)
    request_data = action_service.get_request_data(request, pk)
    
    for key, value in request_data.items():
        if key not in ['created_at', 'updated_at']:
            setattr(instance, key, value)
    
    return action_service.save(request, instance)


@videos_router.POST_request("/<int:pk>/delete", name="videos_delete")
def delete(request: HttpRequest, pk: int):
    instance = view_service.get_one(pk)
    instance.delete()
    return redirect("/admin/videos")