from django.contrib import admin
from django.urls import path
from .views import AuditLogListView
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('audit_log/', AuditLogListView.as_view(), name='audit_log'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)