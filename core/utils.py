import string
from django.db import models
from core.models import Languages
from django.core.paginator import Paginator, EmptyPage
from rest_framework.exceptions import NotFound
from django.core.files.storage import default_storage
from django.core.cache import cache
from django.core.paginator import Paginator
from rest_framework.exceptions import ValidationError as RestValidError
from django.core.exceptions import ValidationError



def paginate_related(queryset, request, page_size="page_size", page="page", allow_empty=True):
    try:
        page_size = request.GET.get(page_size, 20)

        page = request.GET.get(page, 1)

        queryset_paginator = Paginator(queryset, int(page_size))
        queryset_list = queryset_paginator.page(int(page))

        return queryset_list
    except EmptyPage:
        if not allow_empty:
            raise NotFound("detail not found")




# get request.data in JSON
def serialize_request(model, request):
    langs = cache.get('langs')

    if not langs:
        langs = Languages.objects.filter(active=True)
        cache.set("langs", langs)

    data_dict = {}

    for field in model._meta.fields:
        if field.name == 'id':
            continue

        field_dict = {}
        if isinstance(field, models.JSONField):
            for lang in langs:
                field_dict[lang.code] = request.POST.get(f'{field.name}#{lang.code}')
            data_dict[str(field.name)] = field_dict

        elif isinstance(field, models.ForeignKey):
            related_model = field.related_model
            id = request.POST.get(str(field.name))

            if id:
                model = related_model.objects.get(id=int(id))
                data_dict[field.name] = model
            else:
                data_dict[field.name] = None

        else:
            value = request.POST.get(str(field.name))
            if value and not isinstance(field, models.BooleanField):
                data_dict[str(field.name)] = value
                
            elif isinstance(field, models.BooleanField):
                if field.name in request.POST:
                    data_dict[str(field.name)] = True
                elif field.name not in request.POST:
                    data_dict[str(field.name)] = False

            elif not isinstance(field, models.FileField):
                data_dict[str(field.name)] = None
            
    return data_dict


# search_paginate
def search_pagination(request):
    url = request.path + '?'

    if 'q=' in request.get_full_path():
        if '&' in request.get_full_path():
            url = request.get_full_path().split('&')[0] + '&'
        else:
            url = request.get_full_path() + '&'

    return url



# list to queryset
def list_to_queryset(model_list, model):
    if len(model_list) > 0:
        return model_list[0].__class__.objects.filter(
            pk__in=[obj.pk for obj in model_list])
    else:
        return model.objects.none()


# search translations
def search_translation(query, queryset, model):
    langs = Languages.objects.all()
    endlist = []
    if query and query != '':
        query = query.lower()
        for item in queryset:
            for lang in langs:
                if query in str(item.value.get(lang.code, '')).lower() or query in str(item.key).lower() or query in str(item.group.sub_text + '.' + item.key).lower():
                    endlist.append(item)
                continue
    
        queryset = list_to_queryset(endlist, model)
    
    return queryset



# pagination
def paginate(queryset, request, number):
    paginator = Paginator(queryset, number)

    try:
        page_obj = paginator.get_page(request.GET.get("page"))
    except:
        page_obj = paginator.get_page(1)

    return page_obj


# get lst data
def get_lst_data(queryset, request, number, paginator):
    page = request.GET.get('page')

    if page is None or int(page) == 1:
        lst_two = range(1, number + 1)
    else:
        start = (int(page) - 1) * number + 1
        end = int(page) * number

        if end > len(queryset):
            end = len(queryset)

        lst_two = range(start, end + 1)


    return dict(pairs=zip(paginator, lst_two))



# langs save
def lang_save(form, request):
    lang = form.save()
    default_langs = Languages.objects.filter(default=True)
    key = request.POST.get('dropzone-key')
    sess_image = request.session.get(key)

    if not lang.default and not default_langs.exists():
        lang.default = True
        lang.save()


    if sess_image:
        lang.icon = sess_image[0]['name']
        request.session[key].remove(sess_image[0])
        request.session.modified = True
        lang.save()

    return lang


# clean text
def clean_text(str):
    for char in string.punctuation:
        str = str.replace(char, ' ')

    return str.replace(' ', '')



# pre delete ctg images
def predelete_image(keys :list, request, id):
    for key in keys:
        files = request.session.get(key)

        if files:
            for it in list(files):
                if it['id'] == str(id):
                    if default_storage.exists(it['name']):
                        default_storage.delete(it['name'])

                    request.session[key].remove(it)
                    request.session.modified = True

    

# clean session
def clean_session(key, request, id=''):
    sess_images = request.session.get(key)

    if sess_images:
        for item in list(sess_images):
            if str(item['id']) == str(id):
                request.session.get(key).remove(item)
                request.session.modified = True



def format_dropzone_key(model):
    return str(model._meta.verbose_name).replace(" ", "_")


def format_dropzone_key_multiple(model):
    return str(model._meta.verbose_name).replace(" ", "_") + "_multiple"
