from django.contrib import admin

from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "nick_name", "created_at")

    list_display_links = ("email", "nick_name")
