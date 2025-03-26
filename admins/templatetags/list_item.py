from django.template.defaulttags import register


@register.filter
def list_item(list, i):
    try:
        return list[int(i)]
    except:
        return None
