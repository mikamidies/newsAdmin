from django.http import HttpRequest
from api.models import Category
from core.services import ModelViewService, ModelActionService
from core.router import BaseRouter
from django.shortcuts import redirect, render


category_router = BaseRouter("categories")

view_service = ModelViewService(model=Category, search_fields=["title"])
action_service = ModelActionService(model=Category, view_service=view_service,
                                    image_fields=["image"],
                                    template_name="admin/category/form.html",
                                    redirect_to="/admin/categories")


@category_router.GET_request("/", name="category_list")
def list_view(request: HttpRequest):
    queryset = view_service.get_queryset_with_search(request)

    context = view_service.get_list_context_data(request, queryset)

    return render(request, "admin/category/list.html", context=context)


@category_router.GET_request("/create", name="category_create")
def create_get(request: HttpRequest):
    instance = Category()

    action_service.predelete_image(request)

    context = view_service.get_one_context_data(request, instance)

    return render(request, "admin/category/form.html", context=context)


@category_router.POST_request("/create", name="category_create")
def create_post(request: HttpRequest):
    request_data = action_service.get_request_data(request)

    instance = Category(**request_data)

    return action_service.save(request, instance)


@category_router.GET_request("/<int:pk>/edit", name="category_edit")
def edit_get(request: HttpRequest, pk: int):
    instance = view_service.get_one(pk)

    action_service.predelete_image(request, str(pk))

    context = view_service.get_one_context_data(request, instance)

    return render(request, "admin/category/form.html", context=context)


@category_router.POST_request("/<int:pk>/edit", name="category_edit")
def edit_post(request: HttpRequest, pk: int):
    instance = view_service.get_one(pk)

    request_data = action_service.get_request_data(request, pk)

    for key, value in request_data.items():
        setattr(instance, key, value)

    return action_service.save(request, instance)


@category_router.POST_request("/<int:pk>/delete", name="category_delete")
def delete(request: HttpRequest, pk: int):
    instance = view_service.get_one(pk)

    instance.delete()

    return redirect("/admin/categories")
