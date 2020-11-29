from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin-view/', admin.site.urls),
    path('', include('shop.urls')),

]
