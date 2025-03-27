from rest_framework import serializers
from admins.models import StaticInformation
from core.serializers import ThumbnailSerializer

class StaticInformationSerializer(serializers.ModelSerializer):
    # Добавляем alias для изображений
    logo_first = ThumbnailSerializer(alias='thumb')
    logo_second = ThumbnailSerializer(alias='thumb')

    class Meta:
        model = StaticInformation
        fields = "__all__"