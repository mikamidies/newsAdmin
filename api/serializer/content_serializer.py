from rest_framework import serializers
from core.serializers import BaseModelSerializer, ThumbnailSerializer
from api.models import Category, Product, Banner, Media, Slider, Application, News, Videos, Audios, Books

class ProductSerializer(BaseModelSerializer):
    image = ThumbnailSerializer(alias="900x900")

    class Meta:
        model = Product
        fields = "__all__"


class CategorySerializer(BaseModelSerializer):
    image = ThumbnailSerializer(alias="900x900")

    class Meta:
        model = Category
        fields = "__all__"


class CategoryWithProductSerializer(BaseModelSerializer):
    image = ThumbnailSerializer(alias="900x900")
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = "__all__"


class BannerSerializer(BaseModelSerializer):
    image = ThumbnailSerializer(alias="1100x1100")

    class Meta:
        model = Banner
        fields = "__all__"


class MediaSerializer(BaseModelSerializer):
    image = ThumbnailSerializer(alias="1100x1100")

    class Meta:
        model = Media
        fields = "__all__"


class SliderSerializer(serializers.ModelSerializer):
    image = ThumbnailSerializer(alias="1100x1100")

    class Meta:
        model = Slider
        fields = "__all__"


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        exclude = ["status"]

class NewsOthersSerializer(BaseModelSerializer):
    image = ThumbnailSerializer(alias="1100x1100")

    class Meta:
        model = News
        exclude = ["text", "tags"]

class NewsSerializer(BaseModelSerializer):
    image = ThumbnailSerializer(alias="1100x1100")
    others = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        # Удаляем поле others, если оно не нужно
        remove_others = kwargs.pop('remove_others', False)
        super().__init__(*args, **kwargs)
        if remove_others:
            self.fields.pop('others', None)

    def get_others(self, obj):
        others = News.objects.filter(active=True).exclude(pk=obj.pk)[:5]  # Ограничиваем до 5 объектов
        return NewsOthersSerializer(others, many=True, context=self.context).data

class VideosOthersSerializer(BaseModelSerializer):
    class Meta:
        model = Videos
        exclude = ["text", "tags"] 

class VideosSerializer(BaseModelSerializer):
    others = serializers.SerializerMethodField()

    class Meta:
        model = Videos
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        # Удаляем поле others, если оно не нужно
        remove_others = kwargs.pop('remove_others', False)
        super().__init__(*args, **kwargs)
        if remove_others:
            self.fields.pop('others', None)

    def get_others(self, obj):
        others = Videos.objects.filter(active=True).exclude(pk=obj.pk)[:5]  # Ограничиваем до 5 объектов
        return VideosOthersSerializer(others, many=True, context=self.context).data

class AudiosSerializer(BaseModelSerializer):
    class Meta:
        model = Audios
        fields = "__all__"

class BooksOthersSerializer(BaseModelSerializer):
    image = ThumbnailSerializer(alias="1100x1100")

    class Meta:
        model = Books
        exclude = ["text", "tags"]

class BooksSerializer(BaseModelSerializer):
    image = ThumbnailSerializer(alias="1100x1100")
    others = serializers.SerializerMethodField()

    class Meta:
        model = Books
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        # Удаляем поле others, если оно не нужно
        remove_others = kwargs.pop('remove_others', False)
        super().__init__(*args, **kwargs)
        if remove_others:
            self.fields.pop('others', None)

    def get_others(self, obj):
        others = Books.objects.filter(active=True).exclude(pk=obj.pk)[:5]  # Ограничиваем до 5 объектов
        return BooksOthersSerializer(others, many=True, context=self.context).data