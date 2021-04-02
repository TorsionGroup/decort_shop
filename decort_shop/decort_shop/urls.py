from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static

urlpatterns = [
    path('admin-view/', admin.site.urls),
    path('api/', include('shop.api.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('allauth/', include('allauth.urls')),
]

urlpatterns += i18n_patterns(
    path('cart/', include('shop.cart.urls', namespace='cart')),
    path('', include('shop.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
