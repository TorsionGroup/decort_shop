from django.urls import path
from . import views

app_name = 'wishlist'

urlpatterns = [
    path('wishlist/', views.wishlist_detail, name='wishlist_detail'),
    path('add-to-wishlist/<int:product_id>', views.add_to_wishlist, name='add_to_wishlist'),

]
