from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.db import models
from django.conf import settings
from django.db.models import Q, OuterRef, Subquery, Case, When
from django.http import JsonResponse, HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import json
import datetime
from django.views.generic import ListView, DetailView
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse
from .utils import cookieCart, cartData, guestOrder
from .models import *
from .forms import RegistrationForm, ReviewContentForm, RatingContentForm, ReviewProductForm, RatingProductForm


class BrandOffer:
    def get_brands(self):
        return Brand.objects.filter(is_recommended=1)

    def get_offers(self):
        return Offer.objects.all()


class IndexView(BrandOffer, ListView):
    model = Manager
    queryset = Manager.objects.all()
    template_name = 'torsion_shop/index.html'


class ProductView(BrandOffer, ListView):
    model = Product
    queryset = Product.objects.all()
    paginate_by = 20
    template_name = 'torsion_shop/product/product_list.html'


class ProductDetailView(BrandOffer, DetailView):
    model = Product
    context_object_name = 'product_detail'
    template_name = 'torsion_shop/product/product_detail.html'


class NewsView(ListView):
    model = Content
    queryset = Content.objects.filter(category_id=2)
    context_object_name = 'news_list'
    paginate_by = 10
    template_name = 'torsion_shop/news/news_list.html'


class NewsDetailView(DetailView):
    model = Content
    slug_field = 'alias'
    context_object_name = 'news_detail'
    template_name = 'torsion_shop/news/news_detail.html'


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
        form = RatingContentForm(request.POST)
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
    template_name = 'torsion_shop/about-us.html'


class ContactsView(ListView):
    model = Content
    queryset = Content.objects.filter(category_id=5)
    context_object_name = 'contacts_list'
    template_name = 'torsion_shop/contacts.html'


def login(request):
    return render(request, 'torsion_shop/account/login.html')


def account(request):
    return render(request, 'torsion_shop/account/account.html')


def wishlist(request):
    return render(request, 'torsion_shop/wishlist.html')


def faq(request):
    return render(request, 'torsion_shop/faq.html')


class CartView(View):
    def cart(self, request):
        return render(request, 'torsion_shop/cart.html')


def compare(request):
    return render(request, 'torsion_shop/compare.html')


class CheckoutView(View):
    def checkout(self, request):
        return render(request, 'torsion_shop/checkout.html')


class RegistrationView(CreateView):
    template_name = 'torsion_shop/account/login.html'
    form_class = RegistrationForm

    def get_context_data(self, *args, **kwargs):
        context = super(RegistrationView, self).get_context_data(*args, **kwargs)
        context['next'] = self.request.GET.get('next')
        return context

    def get_success_url(self):
        next_url = self.request.POST.get('next')
        success_url = reverse('login')
        if next_url:
            success_url += '?next={}'.format(next_url)

        return success_url


class ProfileView(UpdateView):
    model = Account
    fields = ['username', 'phone', 'date_of_birth', 'picture']
    template_name = 'torsion_shop/account/account.html'

    def get_success_url(self):
        return reverse('index')

    def get_object(self):
        return self.request.user


class ExampleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'status': 'request was permitted'
        }
        return Response(content)


class FilterProductView(ListView):
    paginate_by = 5

    def get_queryset(self):
        queryset = Product.objects.filter(
            Q(brands__in=self.request.GET.getlist('brand')) |
            Q(offers__in=self.request.GET.getlist('offer'))
        ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['brand'] = ''.join([f'brand={x}&' for x in self.request.GET.getlist('brand')])
        context['offer'] = ''.join([f'offer={x}&' for x in self.request.GET.getlist('offer')])
        return context


class Search(ListView):
    paginate_by = 3

    def get_queryset(self):
        return Product.objects.filter(title__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

