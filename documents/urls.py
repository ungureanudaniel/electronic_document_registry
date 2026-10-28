from django.contrib import admin
from django.urls import path

from .views import DocumentListView, dashboard, DocumentUploadView

urlpatterns = [
    path('', DocumentListView.as_view(), name='document_list'),
    path('dashboard/', dashboard, name='dashboard'),
    path('document_upload/', DocumentUploadView.as_view(), name='document_upload'),
]