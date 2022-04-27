from django.shortcuts import render
import json

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


def index(request):
    return render(request, 'mainapp/index.html', context={
        'menu': data['menu'],
        'social_links': data['social_links'],
    })


def products(request):
    return render(request, 'mainapp/products.html', context={
        'menu': data['menu'],
        'social_links': data['social_links'],
        'products': data['products'],
        'products_links': data['products_links'],
    })


def contact(request):
    return render(request, 'mainapp/contact.html', context={
        'menu': data['menu'],
        'social_links': data['social_links'],
    })
