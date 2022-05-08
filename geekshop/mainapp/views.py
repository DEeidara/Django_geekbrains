from django.shortcuts import render, get_object_or_404
import json
from .models import Product, Category
from django.conf import settings

with open((settings.JSON_ROOT / 'data.json'), 'r', encoding='utf-8') as f:
    data = json.load(f)


def index(request):
    return render(request, 'mainapp/index.html', context={
        'menu': data['menu'],
        'social_links': data['social_links'],
    })


def products(request):
    categories = Category.objects.all()
    products = Product.objects.all()[:3]
    return render(request, 'mainapp/products.html', context={
        'menu': data['menu'],
        'social_links': data['social_links'],
        'products': products,
        'categories': categories,
    })


def contact(request):
    return render(request, 'mainapp/contact.html', context={
        'menu': data['menu'],
        'social_links': data['social_links'],
    })


def category(request, pk):
    categories = Category.objects.all()
    category = get_object_or_404(Category, pk=pk)
    products = Product.objects.filter(category=category)
    return render(request, 'mainapp/category.html', context={
        'menu': data['menu'],
        'social_links': data['social_links'],
        'products': products,
        'categories': categories,
        'category': category
    })
