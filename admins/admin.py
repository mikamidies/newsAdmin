from django.contrib import admin
from django.contrib.auth.models import Permission
from admins.models import TranlsationGroups
# Register your models here.

admin.site.register(Permission)

admin.site.register(TranlsationGroups)
