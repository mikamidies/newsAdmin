from admins.models import Translations, StaticInformation
from api.serializer import (
    TranslationSerializer,
    StaticInformationSerializer,
    CategorySerializer,
    BannerSerializer,
    MediaSerializer,
    SliderSerializer,
    CategoryWithProductSerializer,
    ApplicationSerializer, 
    NewsSerializer, VideosSerializer, AudiosSerializer, BooksSerializer
)
from rest_framework import response, views, generics
from rest_framework.response import Response  # Add this import
from api.models import Category, Banner, Media, Slider, Application, News, Videos, Audios, Books
from core.pagination import BasePagination
from rest_framework.generics import RetrieveAPIView
from admins.models import StaticInformation
from core.models import Languages
from rest_framework.parsers import MultiPartParser, FormParser

class StaticInformationView(RetrieveAPIView):
    """API endpoint для получения общих настроек сайта на конкретном языке"""
    
    def get_object(self):
        return StaticInformation.objects.first()

    def get_language_code(self):
        """Получаем код языка из заголовка"""
        default_lang = Languages.objects.filter(default=True).first()
        default_code = default_lang.code if default_lang else 'ru'
        
        lang_code = self.request.headers.get('Accept-Language', default_code).lower()
        language = Languages.objects.filter(code__iexact=lang_code, active=True).first()
        
        return language.code if language else default_code

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return Response({})

        lang_code = self.get_language_code()
        
        response_data = {
            "id": instance.id,
            "logo_first": instance.logo_first.url if instance.logo_first else None,
            "title": instance.title.get(lang_code, ""),
            "subtitle": instance.subtitle.get(lang_code, ""),
            "description": instance.description.get(lang_code, ""),
            "about_us": instance.about_us.get(lang_code, ""),
            "adres": instance.adres.get(lang_code, ""),
            "email": instance.email or "",
            "telegram": instance.telegram or "",
            "instagram": instance.instagram or "",
            "facebook": instance.facebook or "",
            "youtube": instance.youtube or "",
            "nbm": instance.nbm or "",
            "video_url": instance.video_url or ""
        }
        
        return Response(response_data)

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

class NewsList(generics.ListCreateAPIView):
    queryset = News.objects.filter(active=True).order_by("-id")
    serializer_class = NewsSerializer
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        if 'image' in self.request.FILES:
            serializer.save(image=self.request.FILES['image'])
        else:
            serializer.save()

class VideosListView(generics.ListAPIView):
    queryset = Videos.objects.filter(active=True)
    serializer_class = VideosSerializer

class AudiosListView(generics.ListAPIView):
    queryset = Audios.objects.filter(active=True)
    serializer_class = AudiosSerializer

class BooksListView(generics.ListCreateAPIView):
    queryset = Books.objects.filter(active=True)
    serializer_class = BooksSerializer
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        if 'image' in self.request.FILES:
            serializer.save(image=self.request.FILES['image'])
        else:
            serializer.save()
