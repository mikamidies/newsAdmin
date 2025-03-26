from django.db.models import Model
from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404


class ModelBaseService:
    model: Model

    def __init__(self, model: Model) -> None:
        self.model = model

    def get_queryset(self):
        if not self.model:
            raise Exception("model is required in BasedListView")

        queryset = self.model.objects.order_by('-id')

        return queryset


    def get_one(self, pk: int):
        queryset = self.get_queryset();
        return get_object_or_404(queryset, pk=pk)
