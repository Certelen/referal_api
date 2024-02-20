from django.contrib import admin

from .models import Referal, User


@admin.register(Referal)
class ReferalAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
