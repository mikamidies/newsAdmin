import json

from rest_framework.exceptions import status
from admins.serializers import TranslationSerializer
from admins.models import TranlsationGroups, Translations
from core.models import Languages
from core.utils import *
from django.views.generic import ListView, UpdateView, DetailView
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render, get_object_or_404
from django.db import transaction


# translations list
class TranslationList(ListView):
    model = Translations
    template_name = 'admin/translation_list.html'

    def get_queryset(self):
        queryset = Translations.objects.order_by("-id")
        query = self.request.GET.get("q")
        queryset = search_translation(query, queryset, Translations)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(TranslationList, self).get_context_data(**kwargs)
        context['groups'] = TranlsationGroups.objects.all()
        context['langs'] = Languages.objects.filter(
            active=True).order_by('-default')
        context['url'] = search_pagination(self.request)

        # pagination
        paginator = paginate(self.get_queryset(), self.request, 20)

        context['translations'] = get_lst_data(
            self.get_queryset(), self.request, 20, paginator)
        context['page_obj'] = paginator

        context['page_range'] = paginator.paginator.get_elided_page_range(
            number=paginator.number, on_each_side=3, on_ends=2)

        return context


# translation group
class TranslationGroupDetail(DetailView):
    model = TranlsationGroups
    template_name = 'admin/translation_list.html'

    def get_context_data(self, **kwargs):
        context = super(TranslationGroupDetail,
                        self).get_context_data(**kwargs)
        context['groups'] = TranlsationGroups.objects.all()
        context['langs'] = Languages.objects.filter(
            active=True).order_by('-default')
        lst_one = self.object.translations.order_by('-id')

        # search
        query = self.request.GET.get("q")
        lst_one = search_translation(query, lst_one, Translations)

        # range
        lst_two = range(1, len(lst_one) + 1)

        # zip 2 lst
        context['translations'] = dict(pairs=zip(lst_one, lst_two))

        return context


# transtion update
def translation_update(request):
    if request.method == 'GET':
        id = request.GET.get('id')

        try:
            translation = Translations.objects.get(id=int(id))
            serializer = TranslationSerializer(translation)

            return JsonResponse(serializer.data)
        except:
            return JsonResponse({'error': 'error'}, safe=False)

    elif request.method == 'POST':
        data = serialize_request(Translations, request)
        id = request.POST.get("id")

        if "group" in data.keys():
            del data['group']

        try:
            translation = Translations.objects.get(id=int(id))

            for key, value in data.items():
                setattr(translation, key, value)

            translation.full_clean()
            translation.save()
        except ValidationError as e:
            return JsonResponse(e.message_dict)

        serializer = TranslationSerializer(translation)

        return JsonResponse(serializer.data)

    return JsonResponse({"message": "how u evend did this? Method is not allowed!!!"}, status=405)


# add translation group
def add_trans_group(request):
    if request.method == 'POST':
        data_dict = serialize_request(TranlsationGroups, request)

        try:
            transl_group = TranlsationGroups(**data_dict)
            transl_group.full_clean()
            transl_group.save()
        except ValidationError as e:
            return JsonResponse(e.message_dict)

        data = {
            'id': transl_group.pk,
            'name': transl_group.title,
            'key': transl_group.sub_text
        }

        return JsonResponse(data)

    return JsonResponse({"message": "Method is not allowed!"}, status=405)


# translations delete
def delete_translation(request, pk):
    if request.method == "POST":
        object = get_object_or_404(Translations.objects.all(), pk=pk)

        try:
            object.delete()
        except:
            return JsonResponse({"message": "error"}, status=403)

        return JsonResponse({"message": "success"})

    return JsonResponse({"message": "method not allowed"}, status=405)


# add translations from json
@transaction.atomic
def translations_from_json(request):
    if request.method == "POST":
        translations: str = request.POST.get("translations", '')

        transls_json = json.loads(translations)

        if (isinstance(transls_json, dict)):
            for key, value in transls_json.items():
                group_key = key.split(".")[0]
                key = key.split(".")[-1]

                default_lang = Languages.objects.get(default=True)

                json_value = {
                    default_lang.code: value
                }

                group, _ = TranlsationGroups.objects.get_or_create(
                    title=group_key, sub_text=group_key)
                translation, _ = Translations.objects.update_or_create(
                    group=group, key=key, value=json_value)

    return JsonResponse({"message": "success"})


# translation group udate
class TranslationGroupUdpate(UpdateView):
    model = TranlsationGroups
    template_name = 'admin/translation_edit.html'
    fields = '__all__'
    success_url = '/admin/translations'

    def get_context_data(self, **kwargs):
        context = super(TranslationGroupUdpate,
                        self).get_context_data(**kwargs)
        context['groups'] = TranlsationGroups.objects.all()
        context['langs'] = Languages.objects.filter(
            active=True).order_by('-default')
        context['lng'] = Languages.objects.filter(
            active=True).filter(default=True).first()
        lst_one = self.object.translations.all()

        # zip 2 lst
        context['translations'] = enumerate(lst_one, start=1)

        return context

    def collect_translation(self, request, row) -> dict:
        data = {}

        data['group'] = self.object
        data['key'] = request.POST.get(f"key[{row}]")

        value_data = {}

        for lang in self.langs:
            value_data[lang.code] = request.POST.get(
                f"value[{row}][{lang.code}]")

        data['value'] = value_data

        print(value_data)

        return data

    def collect_new_translations(self, request) -> enumerate:
        new_objects = []

        rows_list = request.POST.getlist("rows")

        start_index = 0

        for row in rows_list:
            id = request.POST.get(f"id[{row}]")

            if not id:
                data = self.collect_translation(request, row)

                new_objects.append(data)

                start_index = int(row)

        return enumerate(new_objects, start=start_index)

    def post(self, request, *args, **kwargs):
        context = super().post(request, *args, **kwargs)
        context_data = self.get_context_data()
        self.object = self.get_object()
        self.langs = Languages.objects.filter(active=True).order_by('-default')
        errors = {}

        try:
            with transaction.atomic():
                rows_list = request.POST.getlist("rows")

                for row in rows_list:
                    data = self.collect_translation(request, row)

                    id = request.POST.get(f"id[{row}]", 0)

                    try:
                        transl = Translations.objects.get(id=int(id))
                    except:
                        transl = None

                    if transl:
                        for key, value in data.items():
                            setattr(transl, key, value)

                    else:
                        transl = Translations(**data)

                    try:
                        transl.full_clean()
                        transl.save()

                    except ValidationError as e:
                        errors[row] = e.message_dict

                if errors:
                    print(errors)
                    raise Exception("There is error")

        except Exception as e:
            context_data['errors'] = errors
            context_data['new_objects'] = self.collect_new_translations(
                request)
            return render(request, template_name=self.template_name, context=context_data)

        return redirect("translation_list")
