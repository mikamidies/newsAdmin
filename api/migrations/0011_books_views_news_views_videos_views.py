# Generated by Django 4.1 on 2025-03-28 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_books_slug_news_slug_videos_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='books',
            name='views',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='news',
            name='views',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='videos',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
