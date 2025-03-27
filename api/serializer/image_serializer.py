from rest_framework import serializers

class ImageSerializer(serializers.Serializer):
    """Сериализатор для обработки изображений"""
    url = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()

    def get_url(self, obj):
        if obj:
            return obj.url
        return None

    def get_thumbnail(self, obj):
        if obj:
            try:
                return obj['thumb'].url
            except:
                return None
        return None