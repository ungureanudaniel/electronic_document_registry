from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import DocCategory


@admin.register(DocCategory)
class DocCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    search_fields = ('name', 'is_active',)
    