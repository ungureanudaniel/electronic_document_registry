from django.contrib import admin
from django.urls import path

from .views import document_list, dashboard, DocumentUploadView

urlpatterns = [
    path('', document_list, name='document_list'),
    path('dashboard/', dashboard, name='dashboard'),
    path('document_upload/', DocumentUploadView.as_view(), name='document_upload'),
]