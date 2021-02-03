from django.apps import apps
from django.urls import include, path

from .api_views import *

urlpatterns = [
    path('brand/', BrandListAPIView.as_view(),name='brands')
]