from django.urls import path
import mainapp.views as mainapp

app_name = "mainapp"

urlpatterns = [
    path("", mainapp.products, name="products"),
    path("<int:pk>/", mainapp.category, name="category"),
    path("<int:pk>/<int:page>/", mainapp.category, name="category"),
    path("product/<int:pk>/", mainapp.product, name="product"),
]
