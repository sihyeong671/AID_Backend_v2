# Register your models here.

from django import forms
from django.contrib import admin

from .models import FAQ


class MyForm(forms.ModelForm):
    class Meta:
        widgets = {
            "title": forms.TextInput(attrs={"size": "20"}),
            "content": forms.Textarea(attrs={"cols": "40", "rows": "10", "class": "vLargeTextField"}),
            "category": forms.TextInput(attrs={"size": "20"}),
        }


class FaqAdminForm(admin.ModelAdmin):
    form = MyForm


admin.site.register(FAQ, FaqAdminForm)
