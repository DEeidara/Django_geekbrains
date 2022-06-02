import adminapp.views as adminapp
from django.urls import path

app_name = "adminapp"

urlpatterns = [
    path("users/create/", adminapp.UserCreateView.as_view(), name="user_create"),
    path("users/", adminapp.UserListView.as_view(), name="users"),
    path(
        "users/update/<int:pk>/", adminapp.UserUpdateView.as_view(), name="user_update"
    ),
    path(
        "users/de_activate/<int:pk>/",
        adminapp.user_de_activate,
        name="user_de_activate",
    ),
    path("users/delete/<int:pk>/", adminapp.user_delete, name="user_delete"),
    path(
        "categories/create/",
        adminapp.CategoryCreateView.as_view(),
        name="category_create",
    ),
    path("categories/", adminapp.CategoryListView.as_view(), name="categories"),
    path(
        "categories/update/<int:pk>/",
        adminapp.CategoryUpdateView.as_view(),
        name="category_update",
    ),
    path(
        "categories/de_activate/<int:pk>/",
        adminapp.category_de_activate,
        name="category_de_activate",
    ),
    path(
        "products/<int:category_pk>/create/",
        adminapp.product_create,
        name="product_create",
    ),
    path("products/<int:category_pk>/", adminapp.products, name="products"),
    path(
        "products/update/<int:product_pk>/",
        adminapp.product_update,
        name="product_update",
    ),
    path(
        "products/de_activate/<int:product_pk>/",
        adminapp.product_de_activate,
        name="product_de_activate",
    ),
    path(
        "products/delete/<int:product_pk>/",
        adminapp.product_delete,
        name="product_delete",
    ),
]
