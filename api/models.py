from django.db import models
from core.models import json_field_validate
from easy_thumbnails.fields import ThumbnailerImageField


class Banner(models.Model):
    title: models.JSONField = models.JSONField(
        validators=[json_field_validate])
    image = ThumbnailerImageField(blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)
    active = models.BooleanField(default=True)


class Category(models.Model):
    title: models.JSONField = models.JSONField(
        validators=[json_field_validate])
    order = models.IntegerField(blank=True, null=True)
    active = models.BooleanField(default=True)
    image = ThumbnailerImageField(blank=True, null=True)
    description: models.JSONField = models.JSONField(blank=True, null=True)


class Product(models.Model):
    title: models.JSONField = models.JSONField(
        validators=[json_field_validate])
    description: models.JSONField = models.JSONField(blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products")
    image = ThumbnailerImageField(blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)
    active = models.BooleanField(default=True)


class Slider(models.Model):
    title: models.JSONField = models.JSONField(
        validators=[json_field_validate])
    image = ThumbnailerImageField(blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)
    active = models.BooleanField(default=True)


class Media(models.Model):
    image = ThumbnailerImageField()
    order = models.IntegerField(blank=True, null=True)
    active = models.BooleanField(default=True)


class Application(models.Model):
    STATUS = [('1', "На рассмотрении"),
              ("2", "Рассмотрено"), ("3", "Отклонено")]

    name = models.CharField(max_length=255)
    number = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=STATUS, default="1")
    created_at = models.DateTimeField(auto_now_add=True)

class News(models.Model):
    title = models.JSONField(validators=[json_field_validate])
    subtitle = models.JSONField(blank=True, null=True)
    text = models.JSONField(blank=True, null=True)
    tags = models.JSONField(blank=True, null=True)
    image = ThumbnailerImageField(blank=True, null=True)
    top = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.pk:  # Если запись уже существует (обновление)
            old_instance = News.objects.filter(pk=self.pk).first()
            if old_instance:
                self.created_at = old_instance.created_at  # Сохранение старого значения
        super().save(*args, **kwargs)

class VideoNews(models.Model):
    title = models.JSONField(validators=[json_field_validate])
    text = models.JSONField(blank=True, null=True)
    top = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)
    youtube_url = models.URLField()

class AudioNews(models.Model):
    title = models.JSONField(validators=[json_field_validate])
    text = models.JSONField(blank=True, null=True)
    top = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)
    audio = models.FileField()

class Book(models.Model):
    title = models.JSONField(validators=[json_field_validate])
    image = models.ImageField(blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)
    book = models.FileField()