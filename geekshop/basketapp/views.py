from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from .models import Basket
from mainapp.models import Product


def basket(request):
    return render(request, 'basketapp/basket.html', context={
        'basket': Basket.objects.filter(user=request.user)
    })


def add(request, product_id):
    basket = Basket.objects.filter(user=request.user)
    product = get_object_or_404(Product, pk=product_id)
    if basket:
        basket_item = basket[0]
        basket_item.quantity += 1
        basket_item.save()
    else:
        basket_item = Basket(user=request.user, product=product, quantity=1)
        basket_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'), reverse('index'))


def remove(request, basket_id):
    basket = get_object_or_404(Basket, pk=basket_id)
    basket.quantity -= 1
    if not basket.quantity:
        basket.delete()
    else:
        basket.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'), reverse('index'))
