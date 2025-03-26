from django.template.defaulttags import register

from core.models import Languages


@register.simple_tag(takes_context=True)
def field_value(context, **kwargs):
    instance = context.get('object')
    field = kwargs.get("field")
    lang = kwargs.get("lang", Languages(code="ru"))

    if instance:
        data_dict = instance.__dict__
    else:
        return ""

    result = data_dict.get(field, "")

    
    if isinstance(result, dict):
        result = result.get(lang.code, "")


    return result if result != None else ""
