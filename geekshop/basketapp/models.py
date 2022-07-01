from django.db import models
from mainapp.models import Product
from django.contrib.auth import get_user_model


class BasketManager(models.Manager):
    def total_quantity(self):
        return sum(item.quantity for item in self.all())

    def total_sum(self):
        return sum(item.product.price * item.quantity for item in self.all())

    def can_create_order(self):
        return all(item.quantity <= item.product.quantity for item in self.all())


class Basket(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="basket"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = BasketManager()

    @property
    def cost(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.product} - {self.quantity} pcs"
