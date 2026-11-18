from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import SecureDocumentDeleteView, DocumentListView, Dashboard, DocumentUploadView, \
    DocumentManagementView, SecureCategoryDeleteView, DocumentUpdateView

urlpatterns = [
    path('', Dashboard.as_view(), name='dashboard'),
    path('document_list/', DocumentListView.as_view(), name='document_list'),
    path('document_upload/', DocumentUploadView.as_view(), name='document_upload'),
    
    path('management/documents/', DocumentManagementView.as_view(), name='document_management'),
    path('management/documents/update/<int:pk>/', DocumentUpdateView.as_view(), name='document_update'),
    path('management/documents/<int:pk>/delete/', SecureDocumentDeleteView.as_view(), name='document_secure_delete'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)