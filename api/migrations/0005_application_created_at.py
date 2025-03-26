# Generated by Django 5.0.1 on 2025-01-29 09:19

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0004_application"),
    ]

    operations = [
        migrations.AddField(
            model_name="application",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
