from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, OuterRef, Subquery, Case, When, Sum
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, View
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Greatest

from .models import *
from .forms import SearchForm
from .cart.forms import CartAddProductForm


class BrandsCarsOffers:

    def get_brands(self):
        return Brand.objects.filter(is_recommended=True)

    def get_offers(self):
        return Offer.objects.filter(is_recommended=True)

    def get_manufacturer_name(self):
        manufacturer_name_sorted_list = sorted(
            set(Product.objects.filter(manufacturer_name__isnull=False).values_list('manufacturer_name', flat=True)))
        return manufacturer_name_sorted_list


class IndexView(BrandsCarsOffers, ListView):
    model = Manager
    queryset = Manager.objects.all()
    template_name = 'decort_shop/index.html'


# class ProductView(BrandsCarsOffers, ListView):
#     model = Product
#     queryset = Product.objects.all()
#     context_object_name = 'product_list'
#     paginate_by = 30
#     template_name = 'decort_shop/product/product_list.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['catalogcategories'] = CatalogCategory.objects.all()
#         return context

def catalog_product_list(request, category_slug):
    categories = CatalogCategory.objects.all()
    category = get_object_or_404(CatalogCategory, url=category_slug)
    products = Product.objects.filter(category_id=category)
    paginator = Paginator(products, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj, 'category': category, 'categories': categories, 'products': products
    }
    return render(request, 'decort_shop/product/product_list.html', context)


# class ProductDetailView(BrandsCarsOffers, DetailView):
#     model = Product
#     pk_url_kwarg = 'id'
#     context_object_name = 'product_detail'
#     template_name = 'decort_shop/product/product_detail.html'

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    cart_product_form = CartAddProductForm()
    context = {'product': product, 'cart_product_form': cart_product_form}
    return render(request, 'decort_shop/product/product_detail.html', context)


class CatalogCategoryView(BrandsCarsOffers, ListView):
    model = CatalogCategory
    queryset = CatalogCategory.objects.all()
    context_object_name = 'catalog_category_list'
    template_name = 'decort_shop/product/catalog_category_list.html'


# class CatalogCategoryDetailView(BrandsCarsOffers, ListView):
#     model = CatalogCategory
#     slug_field = 'url'
#     context_object_name = 'catalog_product_detail'
#     paginate_by = 30
#     template_name = 'decort_shop/product/product_list.html'
#
#     def get_queryset(self, **kwargs):
#         return CatalogCategory.objects.filter(id=kwargs.get('category_id'))
#
#     def get_context_data(self, **kwargs):
#         context = super(CatalogCategoryDetailView, self).get_context_data(**kwargs)
#         context['products'] = Product.objects.select_related('category_id')
#         return context


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


class AddReviewProduct(BrandsCarsOffers, View):
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


class AddStarRatingProduct(BrandsCarsOffers, View):
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
def compare(request):
    return render(request, 'decort_shop/product/compare.html')


def faq(request):
    return render(request, 'decort_shop/faq.html')


def product_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data['query']
        results = Product.objects.annotate(
            similarity=Greatest(
                TrigramSimilarity('article', query),
                TrigramSimilarity('specification', query),
                TrigramSimilarity('keywords', query),
                TrigramSimilarity('name_ru', query),
                TrigramSimilarity('name_uk', query),
                TrigramSimilarity('name_en', query))
            ).filter(similarity__gt=0.4).order_by('-similarity')
    return render(request, 'decort_shop/product/product_search.html', {'form': form, 'query': query,
                                                                       'results': results})


class FilterBrandsCarsOffersView(BrandsCarsOffers, ListView):
    def get_queryset(self):
        queryset = Product.objects.filter(

        )
        return queryset
