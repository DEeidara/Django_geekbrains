from django.shortcuts import render
from authapp.models import ShopUser
from adminapp.forms import (
    ShopUserRegistrationForm,
    ShopUserEditForm,
    CategoryCreateEditForm,
    ProductCreateEditForm,
)
from django.shortcuts import get_object_or_404, render
from mainapp.models import Product, Category
from django.http.response import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from adminapp.utils import check_is_superuser
from django.views.generic import ListView, CreateView, UpdateView
from django.utils.decorators import method_decorator


class TitleMixin:
    title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        return context


class SuperUserRequiredMixin:
    @method_decorator(check_is_superuser)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UserListView(SuperUserRequiredMixin, TitleMixin, ListView):
    title = "Users"
    template_name = "adminapp/users.html"
    queryset = ShopUser.objects.order_by("date_joined")


class UserCreateView(SuperUserRequiredMixin, TitleMixin, CreateView):
    title = "Create user"
    template_name = "adminapp/user_create.html"
    model = ShopUser
    form_class = ShopUserRegistrationForm
    success_url = reverse_lazy("admin:users")


class UserUpdateView(SuperUserRequiredMixin, TitleMixin, UpdateView):
    title = "Edit user"
    template_name = "adminapp/user_update.html"
    model = ShopUser
    form_class = ShopUserEditForm
    success_url = reverse_lazy("admin:users")


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


def user_delete(request, pk):
    title = "Delete user"
    user = get_object_or_404(ShopUser, pk=pk)
    if request.method == "POST":
        user.delete()
        return HttpResponseRedirect(reverse("admin:users"))
    content = {"title": title, "user": user}
    return render(request, "adminapp/user_delete.html", content)


class CategoryListView(SuperUserRequiredMixin, TitleMixin, ListView):
    title = "Categories"
    template_name = "adminapp/categories.html"
    model = Category


class CategoryCreateView(SuperUserRequiredMixin, TitleMixin, CreateView):
    title = "Category create"
    model = Category
    template_name = "adminapp/category_create.html"
    success_url = reverse_lazy("admin:categories")
    form_class = CategoryCreateEditForm


class CategoryUpdateView(SuperUserRequiredMixin, TitleMixin, UpdateView):
    title = "Category edit"
    model = Category
    template_name = "adminapp/category_update.html"
    success_url = reverse_lazy("admin:categories")
    form_class = CategoryCreateEditForm


@check_is_superuser
def category_de_activate(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if category.is_active:
        category.is_active = False
        category.save()
    else:
        category.is_active = True
        category.save()
    return HttpResponseRedirect(reverse("admin:categories"))


@check_is_superuser
def products(request, category_pk):
    category = get_object_or_404(Category, pk=category_pk)
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


@check_is_superuser
def product_create(request, category_pk):
    category = get_object_or_404(Category, pk=category_pk)
    form = ProductCreateEditForm(initial={"category": category})
    if request.method == "POST":
        form = ProductCreateEditForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("admin:products", args=[category_pk]))

    content = {"title": "Create product", "form": form, "category": category}
    return render(request, "adminapp/product_create.html", content)


@check_is_superuser
def product_update(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    form = ProductCreateEditForm(instance=product)
    if request.method == "POST":
        form = ProductCreateEditForm(
            data=request.POST, files=request.FILES, instance=product
        )
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse("admin:products", args=[product.category.pk])
            )

    content = {"title": "Edit product", "form": form, "product": product}
    return render(request, "adminapp/product_update.html", content)


@check_is_superuser
def product_de_activate(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    if product.is_active:
        product.is_active = False
        product.save()
    else:
        product.is_active = True
        product.save()
    return HttpResponseRedirect(reverse("admin:products", args=[product.category.pk]))


@check_is_superuser
def product_delete(request, product_pk):
    title = "Delete product"
    product = get_object_or_404(Product, pk=product_pk)
    if request.method == "POST":
        product.delete()
        return HttpResponseRedirect(
            reverse("admin:products", args=[product.category.pk])
        )
    content = {"title": title, "product": product}
    return render(request, "adminapp/product_delete.html", content)
