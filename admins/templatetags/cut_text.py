from django.template.defaulttags import register


@register.filter
def cut_text(strng, count=50):
    if strng is None:
        strng = ''

    if len(str(strng)) > count:
        return strng[:count] + '...'
    else:
        return strng
