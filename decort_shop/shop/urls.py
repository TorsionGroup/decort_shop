from django.apps import apps
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('brand/', views.BrandProductView.as_view(), name='brand'),
    path('news/', views.NewsView.as_view(), name='news'),
    path('news/<slug:slug>/', views.NewsDetailView.as_view(), name='news_detail'),
    path('about-us/', views.AboutUsView.as_view(), name='about-us'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('catalog/', views.CatalogCategoryView.as_view(), name='catalog_category_list'),
    path('catalog/<slug:category_slug>/', views.catalog_product_list, name='catalog_product_detail'),
    path('product/', views.catalog_product_list, name='product_list'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('login/', views.login, name='login'),
    path('account/', views.account, name='account'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('faq/', views.faq, name='faq'),
    path('compare/', views.compare, name='compare'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('add-rating-product/', views.AddStarRatingProduct.as_view(), name='add_rating_product'),
    path('add-rating-content/', views.AddStarRatingContent.as_view(), name='add_rating_content'),
    path('review-product/<int:pk>/', views.AddReviewProduct.as_view(), name='add_review_product'),
    path('review-content/<int:pk>/', views.AddReviewContent.as_view(), name='add_review_content'),
]
