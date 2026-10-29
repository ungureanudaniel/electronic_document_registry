from django.contrib import admin
from django.urls import path
from categories.views import NewCategoryView
from .views import DocumentListView, Dashboard, DocumentUploadView

urlpatterns = [
    path('', Dashboard.as_view(), name='dashboard'),
    path('document_list/', DocumentListView.as_view(), name='document_list'),
    path('document_upload/', DocumentUploadView.as_view(), name='document_upload'),
    path('new_category/', NewCategoryView.as_view(), name='newcategory'),

]