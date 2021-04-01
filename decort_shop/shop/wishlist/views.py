from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect

from .models import *


def wishlist_list(request):
    wishlisted_list = []
    if request.user.is_authenticated:
        wishlisted_list = list(
            Wishlist.objects.filter(user_id=request.user).values_list('product_id', flat=True).order_by('product_id'))
    return render(request, template_name='main/home.html', context={"product": Product.objects.all(),
                                                                    'wishlisted_list': wishlisted_list})


@login_required
def wishlist_detail(request):
    wishlist = {}
    if request.method == "GET":
        if request.user.is_authenticated:
            wishlist = Wishlist.objects.filter(user_id_id=request.user.pk)
        else:
            print("Please login")
            return HttpResponse("login")

    return render(request, template_name='main/wishlist.html', context={"wishlist": wishlist})


@login_required
def add_to_wishlist(request):
    if request.is_ajax() and request.POST and 'attr_id' in request.POST:
        if request.user.is_authenticated:
            data = Wishlist.objects.filter(user_id_id=request.user.pk, music_id_id=int(request.POST['attr_id']))
            if data.exists():
                data.delete()
            else:
                Wishlist.objects.create(user_id_id=request.user.pk, music_id_id=int(request.POST['attr_id']))
    else:
        print("No Product is Found")

    return redirect("main:home")
