from django.http import HttpRequest
from api.models import News
from core.services import ModelViewService, ModelActionService
from core.router import BaseRouter
from django.shortcuts import redirect, render


news_router = BaseRouter("news")

view_service = ModelViewService(model=News, search_fields=["title"])
action_service = ModelActionService(model=News, view_service=view_service,
                                 template_name="admin/news/form.html",
                                 redirect_to="/admin/news", image_fields=["image"])


@news_router.GET_request("/", name="news_list")
def list_view(request: HttpRequest):
    queryset = view_service.get_queryset_with_search(request)
    context = view_service.get_list_context_data(request, queryset)
    return render(request, "admin/news/list.html", context=context)


@news_router.GET_request("/create", name="news_create")
def create_get(request: HttpRequest):
    instance = News()
    context = view_service.get_one_context_data(request, instance)
    action_service.predelete_image(request)
    return render(request, "admin/news/form.html", context=context)


@news_router.POST_request("/create", name="news_create")
def create_post(request: HttpRequest):
    request_data = action_service.get_request_data(request)
    instance = News(**request_data)
    return action_service.save(request, instance)


@news_router.GET_request("/<int:pk>/edit", name="news_edit")
def edit_get(request: HttpRequest, pk: int):
    instance = view_service.get_one(pk)
    context = view_service.get_one_context_data(request, instance)
    action_service.predelete_image(request, str(pk))
    return render(request, "admin/news/form.html", context=context)


@news_router.POST_request("/<int:pk>/edit", name="news_edit")
def edit_post(request: HttpRequest, pk: int):
    instance = view_service.get_one(pk)
    request_data = action_service.get_request_data(request, pk)
    
    for key, value in request_data.items():
        setattr(instance, key, value)
    
    return action_service.save(request, instance)


@news_router.POST_request("/<int:pk>/delete", name="news_delete")
def delete(request: HttpRequest, pk: int):
    instance = view_service.get_one(pk)
    instance.delete()
    return redirect("/admin/news")