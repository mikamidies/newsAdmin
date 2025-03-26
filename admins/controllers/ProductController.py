from django.http import HttpRequest
from api.models import Product, Category
from core.services import ModelViewService, ModelActionService
from core.router import BaseRouter
from django.shortcuts import redirect, render


product_router = BaseRouter("products")

view_service = ModelViewService(model=Product, search_fields=["title"])
action_service = ModelActionService(model=Product, view_service=view_service,
                                    image_fields=["image"],
                                    template_name="admin/product/form.html",
                                    redirect_to="/admin/products")


@product_router.GET_request("/", name="product_list")
def list_view(request: HttpRequest):
    queryset = view_service.get_queryset_with_search(request)

    context = view_service.get_list_context_data(request, queryset)

    return render(request, "admin/product/list.html", context=context)


@product_router.GET_request("/create", name="product_create")
def create_get(request: HttpRequest):
    instance = Product()

    action_service.predelete_image(request)

    context = view_service.get_one_context_data(request, instance)

    context["relateds"] = Category.objects.all()

    return render(request, "admin/product/form.html", context=context)


@product_router.POST_request("/create", name="product_create")
def create_post(request: HttpRequest):
    request_data = action_service.get_request_data(request)

    instance = Product(**request_data)

    return action_service.save(request, instance)


@product_router.GET_request("/<int:pk>/edit", name="product_edit")
def edit_get(request: HttpRequest, pk: int):
    instance = view_service.get_one(pk)

    action_service.predelete_image(request, str(pk))

    context = view_service.get_one_context_data(request, instance)

    context["relateds"] = Category.objects.all()

    return render(request, "admin/product/form.html", context=context)


@product_router.POST_request("/<int:pk>/edit", name="product_edit")
def edit_post(request: HttpRequest, pk: int):
    instance = view_service.get_one(pk)

    request_data = action_service.get_request_data(request, pk)

    for key, value in request_data.items():
        setattr(instance, key, value)

    return action_service.save(request, instance)
