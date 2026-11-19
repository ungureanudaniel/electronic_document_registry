from django.contrib import admin
from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['reg_number', 'timestamp', 'doc_type']
    search_fields = ('reg_number', 'timestamp', 'doc_type')
    ordering = ['-reg_number']
    
