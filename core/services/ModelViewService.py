from django.db.models.base import Model
from django.http.request import HttpRequest
from django.db.models.query import QuerySet
from django.db.models import Q
from core.services import ModelBaseService
from core.utils import *
# Create your views here.


# based list view
class ModelViewService(ModelBaseService):
    search_fields: list = list()

    def __init__(self, model, search_fields: list = list()) -> None:
        super().__init__(model)
        self.search_fields = search_fields


    def search(self, request, queryset, fields: list):
        query = request.GET.get("q", "")

        if query == "": return queryset

        filter_params = Q()

        for field in fields:
            filter_params |= Q(**{f'{field}__iregex': str(query)})

        queryset = queryset.filter(filter_params)

        return queryset


    def get_queryset_with_search(self, request: HttpRequest) -> QuerySet[Model]:
        queryset = self.get_queryset()
        queryset = self.search(request, queryset, self.search_fields)

        return queryset


    def get_list_context_data(self, request: HttpRequest, queryset: QuerySet[Model]):
        context = {}

        paginator = paginate(queryset, request, 20)

        context['objects'] = get_lst_data(queryset, request, 20, paginator)

        context['page_obj'] = paginator
        context['page_range'] = paginator.paginator.get_elided_page_range(
            number=paginator.number, on_each_side=3, on_ends=2)

        context['url'] = search_pagination(request)

        return context


    def get_one_context_data(self, request: HttpRequest, object, errors = None):
        context = {}

        context["object"] = object
        context["errors"] = errors
        context["dropzone_key"] = format_dropzone_key(self.model)

        return context
