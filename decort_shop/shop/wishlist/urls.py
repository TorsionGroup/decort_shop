from django.urls import path
from . import views

app_name = 'wishlist'

urlpatterns = [
    path('', views.wishlist_list, name='wishlist_list'),
    path('wishlist/', views.wishlist_detail, name='wishlist_detail'),
    path('add-to-wishlist/', views.add_to_wishlist, name='add_to_wishlist'),

]
