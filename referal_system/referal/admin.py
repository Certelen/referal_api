from django.contrib import admin

from .models import Referals


@admin.register(Referals)
class ReferalsAdmin(admin.ModelAdmin):
    pass
