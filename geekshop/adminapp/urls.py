import adminapp.views as adminapp
from django.urls import path

app_name = "adminapp"

urlpatterns = [
    path("users/create/", adminapp.user_create, name="user_create"),
    path("users/", adminapp.users, name="users"),
    path("users/update/<int:pk>/", adminapp.user_update, name="user_update"),
    path("users/toggle/<int:pk>/", adminapp.user_de_activate, name="user_delete"),
    path("categories/create/", adminapp.category_create, name="category_create"),
    path("categories/", adminapp.categories, name="categories"),
    path(
        "categories/update/<int:pk>/", adminapp.category_update, name="category_update"
    ),
    path(
        "categories/toggle/<int:pk>/",
        adminapp.category_de_activate,
        name="category_delete",
    ),
    path("products/<int:pk>/create/", adminapp.product_create, name="product_create"),
    path("products/<int:pk>/", adminapp.products, name="products"),
    path("products/update/<int:pk>/", adminapp.product_update, name="product_update"),
    path(
        "products/toggle/<int:pk>/", adminapp.product_de_activate, name="product_delete"
    ),
]
