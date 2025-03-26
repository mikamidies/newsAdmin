from django.core.cache import cache
from core.models import Languages



def language_context(request):
    context = {}

    langs = Languages.objects.filter(active=True).order_by('-default')

    context['langs'] = langs

    default_lang = cache.get('default_lang')

    if not default_lang:
        default_lang = langs.filter(default=True).first()

        if default_lang:
            cache.set("default_lang", default_lang)
        else:
            default_lang = {
                "code": ""
            }

    context['lang'] = default_lang

    return context
