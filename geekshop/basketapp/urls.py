from django.urls import path
import basketapp.views as basketapp

app_name = 'basketapp'

urlpatterns = [
    path('', basketapp.basket, name='basket'),
    path('add/<int:product_id>', basketapp.add, name='add'),
    path('remove/<int:basket_id>', basketapp.remove, name='remove'),
]
