from django.http import HttpRequest
from api.models import Books
from core.services import ModelViewService, ModelActionService
from core.router import BaseRouter
from django.shortcuts import redirect, render


books_router = BaseRouter("books")

view_service = ModelViewService(model=Books, search_fields=["title"])
action_service = ModelActionService(model=Books, view_service=view_service,
                                 template_name="admin/books/form.html",
                                 redirect_to="/admin/books",
                                 image_fields=["image", "book"])  # Обрабатываем оба файловых поля


@books_router.GET_request("/", name="books_list")
def list_view(request: HttpRequest):
    queryset = view_service.get_queryset_with_search(request)
    context = view_service.get_list_context_data(request, queryset)
    return render(request, "admin/books/list.html", context=context)


@books_router.GET_request("/create", name="books_create")
def create_get(request: HttpRequest):
    instance = Books()
    context = view_service.get_one_context_data(request, instance)
    action_service.predelete_image(request)  # Очищаем временные файлы
    return render(request, "admin/books/form.html", context=context)


@books_router.POST_request("/create", name="books_create")
def create_post(request: HttpRequest):
    request_data = action_service.get_request_data(request)
    instance = Books(**request_data)
    return action_service.save(request, instance)


@books_router.GET_request("/<int:pk>/edit", name="books_edit")
def edit_get(request: HttpRequest, pk: int):
    instance = view_service.get_one(pk)
    context = view_service.get_one_context_data(request, instance)
    action_service.predelete_image(request, str(pk))  # Очищаем временные файлы
    return render(request, "admin/books/form.html", context=context)


@books_router.POST_request("/<int:pk>/edit", name="books_edit")
def edit_post(request: HttpRequest, pk: int):
    instance = view_service.get_one(pk)
    request_data = action_service.get_request_data(request, pk)
    
    # Сохраняем старые файлы, если новые не были загружены
    if not request.FILES.get('book'):
        request_data['book'] = instance.book
    if not request_data.get('image'):
        request_data['image'] = instance.image

    for key, value in request_data.items():
        if key not in ['created_at', 'updated_at']:
            setattr(instance, key, value)
    
    return action_service.save(request, instance)


@books_router.POST_request("/<int:pk>/delete", name="books_delete")
def delete(request: HttpRequest, pk: int):
    instance = view_service.get_one(pk)
    instance.delete()
    return redirect("/admin/books")