from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import Basket
from mainapp.models import Product, Category
import json

with open((settings.JSON_ROOT / 'data.json'), 'r', encoding='utf-8') as f:
    data = json.load(f)


@login_required
def basket(request):
    categories = Category.objects.all()
    return render(request, 'basketapp/basket.html', context={
        'categories': categories,
        'menu': data['menu'],
        'social_links': data['social_links'],
    })


@login_required
def add(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    basket = Basket.objects.filter(user=request.user, product=product).first()

    if not basket:
        basket = Basket(user=request.user, product=product)
    basket.quantity += 1
    basket.save()
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('product', args=[product_id]))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'), reverse('index'))


@login_required
def remove(request, basket_id):
    basket = get_object_or_404(Basket, pk=basket_id)
    basket.quantity -= 1
    if not basket.quantity:
        basket.delete()
    else:
        basket.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'), reverse('index'))


@login_required
def edit(request, basket_id, quantity):
    basket = get_object_or_404(Basket, pk=basket_id)
    basket.quantity = quantity
    if not basket.quantity:
        basket.delete()
    else:
        basket.save()
    return render(request, 'basketapp/includes/inc_basket_list.html')
