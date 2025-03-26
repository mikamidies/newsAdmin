from typing import Any
from django.core.exceptions import ValidationError
from django.db.models import Model
from django.http.request import HttpRequest
from django.shortcuts import redirect, render
from core.services.RequestDataExtractService import RequestDataExtractService
from django.core.files.storage import default_storage

from core.utils import format_dropzone_key_multiple


class ModelActionService(RequestDataExtractService):
    def __init__(self, model, template_name: str, redirect_to: str, fields=[], exclude=[], image_fields: list = list(), view_service=None) -> None:
        self.model = model
        self.fields = fields
        self.exclude = exclude
        self.view_service = view_service
        self.template_name = template_name
        self.redirect_to = redirect_to
        self.image_fields = image_fields

    def predelele_image_from_session(self, key: str, request, id=""):
        files = request.session.get(key)

        if files:
            print(files)
            for it in list(files):
                if it['id'] == str(id):
                    if default_storage.exists(it['name']):
                        default_storage.delete(it['name'])

                    request.session[key].remove(it)
                    request.session.modified = True

    # pre delete ctg images

    def predelete_image(self, request, id=""):
        if not id:
            id = ""
        for field_name in self.image_fields:
            key = self.get_dropzone_key(field_name)
            self.predelele_image_from_session(key, request, id)

    # delete image from session

    def delete_image_from_session(self, key: str, request, id: Any = ""):
        if not id:
            id = ""
        sess_images = request.session.get(key)

        if sess_images:
            for item in list(sess_images):
                if str(item['id']) == str(id):
                    request.session.get(key).remove(item)
                    request.session.modified = True

    # clean session
    def clean_session(self, request, id=''):
        for field_name in self.image_fields:
            key = self.get_dropzone_key(field_name)
            self.delete_image_from_session(key, request, id)

    def get_validation_errors(self, model: Model):
        try:
            model.full_clean()
        except ValidationError as error:
            return error.message_dict

        return None

    def get_images(self, request, key, id=None):
        if not id:
            id = ""
        return [it for it in request.session.get(key, []) if it['id'] == str(id)]

    def save_multiple_images(self, request: HttpRequest, image_model, parent: Model, pk=None):
        if not image_model:
            return

        key = format_dropzone_key_multiple(image_model)

        images = self.get_images(request, key, id=pk)

        for image in images:
            image = image_model(parent=parent, image=image['name'])
            image.full_clean()
            image.save()

        self.delete_image_from_session(key, request, pk)

    # save model

    def save(self, request: HttpRequest, instance, extra_context: dict | None = None):
        assert self.view_service is not None

        id = instance.id if instance.id else ""

        errors = self.get_validation_errors(instance)

        if errors:
            context: dict = self.view_service.get_one_context_data(
                request,
                instance, errors
            )

            if extra_context:
                context.update(extra_context)

            return render(request, self.template_name, context=context)

        instance.save()

        self.clean_session(request, id)

        return redirect(self.redirect_to)
