from django.shortcuts import render, get_object_or_404
from .models import Product, Category
import random
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page


def index(request):
    return render(
        request,
        "mainapp/index.html",
    )


def products(request):
    products = Product.objects.all()
    hot_product = random.choice(products)
    products = products.exclude(pk=hot_product.pk)[:3]
    return render(
        request,
        "mainapp/products.html",
        context={
            "hot_product": hot_product,
            "products": products,
        },
    )


def product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(
        request,
        "mainapp/product.html",
        context={
            "product": product,
            "category": product.category,
        },
    )


@cache_page(3600)
def contact(request):
    return render(
        request,
        "mainapp/contact.html",
    )


def category(request, pk, page=1):
    category = get_object_or_404(Category, pk=pk)
    products = Product.objects.filter(category=category).order_by("price")
    paginator = Paginator(products, per_page=3)

    if page > paginator.num_pages:
        return HttpResponseRedirect(reverse("category", args=[category.pk]))
    return render(
        request,
        "mainapp/category.html",
        context={
            "products": paginator.page(page),
            "category": category,
        },
    )
