from django.template.defaulttags import register
from django.core.files.storage import default_storage


@register.filter
def exists(file):
    return default_storage.exists(file)