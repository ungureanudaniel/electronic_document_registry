from django.urls import path

from documents.views import SecureCategoryDeleteView
from .views import CategoryManagementView, CategoryUpdateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('management/categories/', CategoryManagementView.as_view(), name='category_management'),
    path('management/categories/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('management/categories/<int:pk>/delete/', SecureCategoryDeleteView.as_view(), name='category_secure_delete'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)