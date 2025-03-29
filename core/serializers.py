from rest_framework import serializers
from core.utils import *
from django.conf import settings
from django.core.files.storage import default_storage
from easy_thumbnails.templatetags.thumbnail import get_thumbnailer
from django.core.cache import cache


class ThumbnailSerializer(serializers.BaseSerializer):
    def __init__(self, alias, instance=None, **kwargs):
        super().__init__(instance, **kwargs)
        self.alias = alias

    def to_representation(self, instance):
        alias = settings.THUMBNAIL_ALIASES.get('').get(self.alias)
        if alias is None:
            return None

        size = alias.get('size')
        url = None

        if instance and default_storage.exists(instance.path):
            orig_url = instance.path.split('.')
            thb_url = '.'.join(orig_url) + \
                f'.{size[0]}x{size[1]}_q85.{settings.THUMBNAIL_EXTENSION}'
            if default_storage.exists(thb_url):
                last_url = instance.url.split('.')
                url = '.'.join(last_url) + \
                    f'.{size[0]}x{size[1]}_q85.{settings.THUMBNAIL_EXTENSION}'
            else:
                url = get_thumbnailer(instance)[self.alias].url

        if url == '' or url is None:
            return None

        request = self.context.get('request', None)
        if request is not None:
            return request.build_absolute_uri(url)

        return url




# get youtube video id
def get_youtube_id(url: str):
    if url:
        url_end = None

        if "https://www.youtube.com/" in url or "https://youtu.be/" in url:
            if "watch?v=" in url:
                url_end = url.split("watch?v=")[-1]

            elif "embed" not in url:
                url_end = url.split("/")[-1]

            return url_end

    return None



# news video serializer
class VideoSerializer(serializers.Serializer):
    def to_representation(self, instance):
        url_end = get_youtube_id(instance)

        if url_end:
            instance = f"https://www.youtube.com/embed/{url_end}"
            return instance

        return None



# get default language
def get_default_lang():
    default_lang = cache.get("def_lang")

    if not default_lang:
        default_lang = Languages.objects.filter(default=True).first()
        cache.set("def_lang", default_lang)

    if default_lang:
        default_lang = default_lang.code
    else:
        default_lang = ''

    return default_lang


# field lang serializer
class JsonFieldSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        language = self.context['request'].headers.get('Language')

        langs = cache.get("languages")
        default_lang = get_default_lang()

        if not langs:
            langs = Languages.objects.filter(active=True)
            cache.set("languages", langs)

        active_lang_codes = [lang.code for lang in langs]

        if not language or language not in active_lang_codes:
            language = default_lang

        data = instance.get(language)

        if data is None or data == '':
            data = instance.get(default_lang)

        return data


# base translatable serializer
class BaseModelSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data_dict = instance.__dict__
        serializer_fields = self.get_fields()
        model_fields = [
            it for it in instance._meta.fields if it.name in serializer_fields]

        for field in model_fields:
            if isinstance(field, models.JSONField):
                value = JsonFieldSerializer(data_dict.get(
                    field.name, {}), context=self.context).data
                data[field.name] = value

        return data

