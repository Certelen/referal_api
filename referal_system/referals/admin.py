from django.contrib import admin

from .models import Referal


@admin.register(Referal)
class ReferalAdmin(admin.ModelAdmin):
    pass
