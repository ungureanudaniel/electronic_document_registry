from django.contrib import admin
from django.urls import path

from .views import DocumentListView, DocumentListView, DocumentUploadView

urlpatterns = [
    path('', DocumentListView.as_view(), name='document_list'),
    path('dashboard/', DocumentListView.as_view(), name='dashboard'),
    path('document_upload/', DocumentUploadView.as_view(), name='document_upload'),
]