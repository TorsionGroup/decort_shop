from django.apps import apps
from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('orders/', include('shop.orders.urls', namespace='orders')),
    path('', views.IndexView.as_view(), name='home'),
    path('news/', views.NewsView.as_view(), name='news'),
    path('news/<slug:slug>/', views.NewsDetailView.as_view(), name='news_detail'),
    path('about-us/', views.AboutUsView.as_view(), name='about-us'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('catalog/', views.CatalogCategoryView.as_view(), name='catalog_category_list'),
    path('catalog/<slug:category_slug>/', views.catalog_product_list, name='catalog_product_detail'),
    path('product/', views.catalog_product_list, name='product_list'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('account/', views.dashboard, name='dashboard'),
    path('account-orders/', views.account_orders, name='account_orders'),
    path('addresses/', views.addresses, name='addresses'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('faq/', views.faq, name='faq'),
    path('compare/', views.compare, name='compare'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('add-rating-product/', views.AddStarRatingProduct.as_view(), name='add_rating_product'),
    path('add-rating-content/', views.AddStarRatingContent.as_view(), name='add_rating_content'),
    path('review-product/<int:pk>/', views.AddReviewProduct.as_view(), name='add_review_product'),
    path('review-content/<int:pk>/', views.AddReviewContent.as_view(), name='add_review_content'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
