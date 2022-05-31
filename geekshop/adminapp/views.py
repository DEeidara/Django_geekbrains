from django.shortcuts import render
from authapp.models import ShopUser
from adminapp.forms import (
    ShopUserRegistrationForm,
    ShopUserEditForm,
    CategoryCreateEditForm,
)
from django.shortcuts import get_object_or_404, render
from mainapp.models import Product, Category
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from adminapp.utils import check_is_superuser


@check_is_superuser
def users(request):
    users_list = ShopUser.objects.all()
    return render(
        request,
        "adminapp/users.html",
        context={"title": "Users", "objects": users_list},
    )


@check_is_superuser
def user_create(request):
    form = ShopUserRegistrationForm()
    if request.method == "POST":
        form = ShopUserRegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("admin:users"))

    content = {"title": "User creation", "form": form}
    return render(request, "adminapp/user_create.html", content)


@check_is_superuser
def user_update(request, pk):
    user = get_object_or_404(ShopUser, pk=pk)
    form = ShopUserEditForm(instance=user)
    if request.method == "POST":
        form = ShopUserEditForm(data=request.POST, files=request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("admin:users"))

    content = {"title": "Edit user", "form": form, "user": user}
    return render(request, "adminapp/user_update.html", content)


@check_is_superuser
def user_de_activate(request, pk):
    user = get_object_or_404(ShopUser, pk=pk)
    if user.is_active:
        user.is_active = False
        user.save()
    else:
        user.is_active = True
        user.save()
    return HttpResponseRedirect(reverse("admin:users"))


@check_is_superuser
def categories(request):
    categories_list = Category.objects.all()
    return render(
        request,
        "adminapp/categories.html",
        context={"title": "Categories", "objects": categories_list},
    )


@check_is_superuser
def category_create(request):
    form = CategoryCreateEditForm()
    if request.method == "POST":
        form = CategoryCreateEditForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("admin:categories"))

    content = {"title": "Category creation", "form": form}
    return render(request, "adminapp/category_create.html", content)


@check_is_superuser
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    form = CategoryCreateEditForm(instance=category)
    if request.method == "POST":
        form = CategoryCreateEditForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("admin:categories"))

    content = {"title": "Edit category", "form": form, "category": category}
    return render(request, "adminapp/category_update.html", content)


@check_is_superuser
def category_de_activate(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.is_active = False
    category.save()
    return HttpResponseRedirect(reverse("admin:categories"))


@check_is_superuser
def products(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products_list = Product.objects.filter(category=category)
    return render(
        request,
        "adminapp/products.html",
        context={
            "title": category.name,
            "category": category,
            "objects": products_list,
        },
    )


def product_create(request, pk):
    pass


def product_update(request, pk):
    pass


def product_de_activate(request, pk):
    pass
