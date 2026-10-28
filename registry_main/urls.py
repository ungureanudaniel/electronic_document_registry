from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
]
urlpatterns.extend([
    path('users/', include('users.urls')),
    path('audit/', include('audit.urls')),
    path('categories/', include('categories.urls')),
    path('', include('documents.urls')),
    path('workflows/', include('workflows.urls')),
])
# ------------add custom media path for production mode-----------
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Option B: For production with custom view
else:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)