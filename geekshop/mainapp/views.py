from django.shortcuts import render
import json
from .models import Product, Category

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


def index(request):
    return render(request, 'mainapp/index.html', context={
        'menu': data['menu'],
        'social_links': data['social_links'],
    })


def products(request):
    categories = Category.objects.all()[:6]
    products = Product.objects.all()[:3]
    return render(request, 'mainapp/products.html', context={
        'menu': data['menu'],
        'social_links': data['social_links'],
        'products': products,
        'categories': categories,
        'products_links': data['products_links'],
    })


def contact(request):
    return render(request, 'mainapp/contact.html', context={
        'menu': data['menu'],
        'social_links': data['social_links'],
    })
