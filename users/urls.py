from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.static import serve
from .views import CustomLogoutView, CustomSignupView, CustomLoginView, UserListView, approve_user, revoke_user, delete_user
from django.utils.translation import gettext_lazy as _

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('user_list/', UserListView.as_view(), name='userlist'),
    path('signup/', CustomSignupView.as_view(), name='signup'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('approve_user/<int:pk>', approve_user, name='approve_user'),
    path('revoke_user/<int:pk>', revoke_user, name='revoke_user'),
    path('delete_user/<int:pk>', delete_user, name='delete_user'),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)