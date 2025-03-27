from django.http import HttpRequest
from api.models import Audios
from core.services import ModelViewService, ModelActionService
from core.router import BaseRouter
from django.shortcuts import redirect, render


audios_router = BaseRouter("audios")

view_service = ModelViewService(model=Audios, search_fields=["title"])
action_service = ModelActionService(model=Audios, view_service=view_service,
                                 template_name="admin/audios/form.html",
                                 redirect_to="/admin/audios",
                                 image_fields=["audio"])  # Используем image_fields вместо file_fields


@audios_router.GET_request("/", name="audios_list")
def list_view(request: HttpRequest):
    queryset = view_service.get_queryset_with_search(request)
    context = view_service.get_list_context_data(request, queryset)
    return render(request, "admin/audios/list.html", context=context)


@audios_router.GET_request("/create", name="audios_create")
def create_get(request: HttpRequest):
    instance = Audios()
    context = view_service.get_one_context_data(request, instance)
    action_service.predelete_image(request)  # Используем predelete_image
    return render(request, "admin/audios/form.html", context=context)


@audios_router.POST_request("/create", name="audios_create")
def create_post(request: HttpRequest):
    request_data = action_service.get_request_data(request)
    instance = Audios(**request_data)
    return action_service.save(request, instance)


@audios_router.GET_request("/<int:pk>/edit", name="audios_edit")
def edit_get(request: HttpRequest, pk: int):
    instance = view_service.get_one(pk)
    context = view_service.get_one_context_data(request, instance)
    action_service.predelete_image(request, str(pk))  # Используем predelete_image
    return render(request, "admin/audios/form.html", context=context)


@audios_router.POST_request("/<int:pk>/edit", name="audios_edit")
def edit_post(request: HttpRequest, pk: int):
    instance = view_service.get_one(pk)
    request_data = action_service.get_request_data(request, pk)
    
    # Сохраняем старый аудио файл, если новый не был загружен
    if not request.FILES.get('audio'):
        request_data['audio'] = instance.audio

    for key, value in request_data.items():
        if key not in ['created_at', 'updated_at']:
            setattr(instance, key, value)
    
    return action_service.save(request, instance)


@audios_router.POST_request("/<int:pk>/delete", name="audios_delete")
def delete(request: HttpRequest, pk: int):
    instance = view_service.get_one(pk)
    instance.delete()
    return redirect("/admin/audios")