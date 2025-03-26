from admins.models import Translations, StaticInformation
from api.serializer import (
    TranslationSerializer,
    StaticInformationSerializer,
    CategorySerializer,
    BannerSerializer,
    MediaSerializer,
    SliderSerializer,
    CategoryWithProductSerializer,
    ApplicationSerializer
)
from rest_framework import response, views, generics
from api.models import Category, Banner, Media, Slider, Application
from core.pagination import BasePagination


# static information
class StaticInfView(views.APIView):
    def get(self, request, format=None):
        obj, _ = StaticInformation.objects.get_or_create(id=1)
        serializer = StaticInformationSerializer(
            obj, context={'request': request})

        return response.Response(serializer.data)


# translations
class TranslationsView(views.APIView):
    def get(self, request, fromat=None):
        translations = Translations.objects.all()
        serializer = TranslationSerializer(
            translations, context={'request': request})
        return response.Response(serializer.data)


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.order_by("order")
    serializer_class = CategorySerializer
    pagination_class = BasePagination


class ProductCategoryList(generics.ListAPIView):
    queryset = Category.objects.order_by("order").prefetch_related("products")
    serializer_class = CategoryWithProductSerializer


class BannerList(generics.ListAPIView):
    queryset = Banner.objects.order_by("order")
    serializer_class = BannerSerializer


class MediaList(generics.ListAPIView):
    queryset = Media.objects.order_by("order")
    serializer_class = MediaSerializer


class SliderList(generics.ListAPIView):
    queryset = Slider.objects.order_by("order")
    serializer_class = SliderSerializer


class ApplicationView(generics.CreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
