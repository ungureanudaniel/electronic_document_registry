from django.urls import path
from .views import CategoryDeleteView, CategoryUpdateView, NewCategoryView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('new_category/', NewCategoryView.as_view(), name='newcategory'),
    path('category/<int:pk>/update/', CategoryUpdateView.as_view(), name='updatecategory'),
    path('category/<int:pk>/delete/', CategoryDeleteView.as_view(), name='deletecategory'),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)