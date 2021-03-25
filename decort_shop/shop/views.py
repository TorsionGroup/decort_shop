from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, OuterRef, Subquery, Case, When, Sum
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, View
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import ReviewContentForm, RatingContentForm, ReviewProductForm, RatingProductForm
from .cart.forms import CartAddProductForm


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
    cart_product_form = CartAddProductForm()
    return render(request, 'decort_shop/product/product_detail.html',
                  {'product': product, 'cart_product_form': cart_product_form})


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


@login_required
def dashboard(request):
    return render(request, 'decort_shop/account/dashboard.html', {'section': 'dashboard'})


@login_required
def addresses(request):
    return render(request, 'decort_shop/account/addresses.html', {'section': 'addresses'})


@login_required
def account_orders(request):
    return render(request, 'decort_shop/account/order.html', {'section': 'account_orders'})


@login_required
def wishlist(request):
    return render(request, 'decort_shop/account/wishlist.html')


@login_required
def compare(request):
    return render(request, 'decort_shop/product/compare.html')


def faq(request):
    return render(request, 'decort_shop/faq.html')

