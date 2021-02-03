from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static

urlpatterns = [
    path('admin-view/', admin.site.urls),
    path('api/', include('shop.api.urls')),
]

urlpatterns += i18n_patterns(
    path('accounts/', include('allauth.urls')),
    path('', include('shop.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
