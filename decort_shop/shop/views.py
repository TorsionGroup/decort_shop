from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from django.db import models, transaction
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q, OuterRef, Subquery, Case, When, Sum
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import json
import datetime
from django.views.generic import ListView, DetailView, View
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from importlib import import_module
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import *
from .forms import ReviewContentForm, RatingContentForm, ReviewProductForm, RatingProductForm


class BrandOffer:
    def get_brands(self):
        return Brand.objects.filter(is_recommended=1)

    def get_offers(self):
        return Offer.objects.all()


class IndexView(BrandOffer, ListView):
    model = Manager
    queryset = Manager.objects.all()
    template_name = 'decort_shop/index.html'


def catalog_product_list(request, category_slug=None):
    category = None
    categories = CatalogCategory.objects.all()
    products = Product.objects.all()
    paginator = Paginator(products, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if category_slug:
        category = get_object_or_404(CatalogCategory, url=category_slug)
        products = products.filter(category_id=category)
    return render(request, 'decort_shop/product/product_list.html',
                  {'page_obj': page_obj, 'category': category, 'categories': categories, 'products': products})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'decort_shop/product/product_detail.html', {'product': product})


class CatalogCategoryView(BrandOffer, ListView):
    model = CatalogCategory
    queryset = CatalogCategory.objects.all()
    context_object_name = 'catalog_category_list'
    template_name = 'decort_shop/product/catalog_category_list.html'


class NewsView(ListView):
    model = Content
    queryset = Content.objects.filter(category_id=2)
    context_object_name = 'news_list'
    paginate_by = 10
    template_name = 'decort_shop/news/news_list.html'


class NewsDetailView(DetailView):
    model = Content
    slug_field = 'alias'
    context_object_name = 'news_detail'
    template_name = 'decort_shop/news/news_detail.html'


class AddReviewContent(View):
    def post(self, request, pk):
        form = ReviewContentForm(request.POST)
        content = Content.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.content = content
            form.save()
        return redirect(content.get_absolute_url())


class AddStarRatingContent(View):
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingContentForm(request.POST)
        if form.is_valid():
            RatingProduct.objects.update_or_create(
                ip=self.get_client_ip(request),
                shop_id=int(request.POST.get('news')),
                defaults={'star_id': int(request.POST.get('star'))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


class AddReviewProduct(View):
    def post(self, request, pk):
        form = ReviewProductForm(request.POST)
        product = Product.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.product = product
            form.save()
        return redirect(product.get_absolute_url())


class AddStarRatingProduct(View):
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingProductForm(request.POST)
        if form.is_valid():
            RatingProduct.objects.update_or_create(
                ip=self.get_client_ip(request),
                news_id=int(request.POST.get('product')),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


class AboutUsView(ListView):
    model = Content
    queryset = Content.objects.filter(category_id=4)
    context_object_name = 'aboutus_list'
    template_name = 'decort_shop/about-us.html'


class ContactsView(ListView):
    model = Content
    queryset = Content.objects.filter(category_id=5)
    context_object_name = 'contacts_list'
    template_name = 'decort_shop/contacts.html'


def login(request):
    return render(request, 'decort_shop/account/login.html')


def account(request):
    return render(request, 'decort_shop/account/account.html')


def wishlist(request):
    return render(request, 'decort_shop/wishlist.html')


def faq(request):
    return render(request, 'decort_shop/faq.html')


def compare(request):
    return render(request, 'decort_shop/compare.html')


def cart(request):
    return render(request, 'decort_shop/cart/cart_detail.html')


def checkout(request):
    return render(request, 'decort_shop/cart/checkout.html')

