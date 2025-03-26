from django.db.models.base import Model
from django.db import models
from django.http.request import HttpRequest
from easy_thumbnails.fields import ThumbnailerImageField
from core.utils import format_dropzone_key
from django.core.cache import cache
from core.models import Languages
from typing import Any


class RequestDataExtractService:
    model: Model
    fields = "__all__"
    exclude = None

    def __init__(self, model, fields: list | None = None, exclude: list | None = None) -> None:
        self.model = model
        self.fields = fields
        self.exclude = exclude

    def get_dropzone_key(self, field_name: str):
        model_key = format_dropzone_key(self.model)
        return f"{model_key}_{field_name}"

    def get_fields_list(self) -> list:
        fields = list()

        for field in self.model._meta.fields:
            if field.name == "id":
                continue

            if (self.exclude != None and field.name not in self.exclude) or field.name in self.fields or (self.exclude == None and self.fields == None):
                fields.append(field)

        return fields

    def get_image(self, request, field_name, id=None):
        if not id:
            id = ""

        key = self.get_dropzone_key(field_name)

        files = [it for it in request.session.get(
            key, []) if str(it.get("id", 0)) == str(id)]

        if len(files):
            return files[0]["name"]

        return None

    def get_request_data(self, request: HttpRequest, id=None):
        fields = self.get_fields_list()
        request_data: dict[str, Any] = {}

        langs = cache.get('langs')

        if not langs:
            langs = Languages.objects.filter(active=True)
            cache.set("langs", langs)

        request_post = request.POST

        for field in fields:
            value = request_post.get(field.name)

            if not value or value == "":
                value = field.get_default()

            if isinstance(field, models.JSONField):
                field_dict = {}

                for lang in langs:
                    field_dict[lang.code] = request.POST.get(
                        f'{field.name}#{lang.code}')

                request_data[str(field.name)] = field_dict

            elif isinstance(field, models.ForeignKey):
                if not value:
                    continue

                related_model = field.related_model
                request_data[field.name] = related_model.objects.filter(
                    id=int(value)).first()

            elif isinstance(field, models.BooleanField):
                request_data[field.name] = value is not None

            elif isinstance(field, ThumbnailerImageField):
                image = self.get_image(request, field.name, id)
                if image:
                    request_data[field.name] = image

            elif isinstance(field, models.FileField):
                request_data[field.name] = request.FILES.get(field.name)

            else:
                request_data[field.name] = value

        return request_data
