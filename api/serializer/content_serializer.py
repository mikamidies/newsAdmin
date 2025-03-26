from rest_framework import serializers
from core.serializers import BaseModelSerializer, ThumbnailSerializer
from api.models import Category, Product, Banner, Media, Slider, Application


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
