from django.contrib import admin
from rest_framework.authtoken.models import Token

from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "nick_name", "created_at")

    list_display_links = "email"


admin.site.register(Token)
