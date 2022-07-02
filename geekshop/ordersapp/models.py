from django.db import models
from django.contrib.auth import get_user_model
from mainapp.models import Product
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete


class Order(models.Model):
    CREATED = "CREATED"
    PAID = "PAID"
    SENT = "SENT"
    DELIVERED = "DELIVERED"
    CANCELED = "CANCELED"

    STATUSES = [
        (CREATED, "Created"),
        (PAID, "Paid"),
        (SENT, "Sent"),
        (DELIVERED, "Delivered"),
        (CANCELED, "Canceled"),
    ]
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="orders"
    )
    status = models.CharField(max_length=16, choices=STATUSES, default="CREATED")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"№{self.id}"

    def get_total_quantity(self):
        items = self.order_items.select_related()
        return sum(list(map(lambda x: x.quantity, items)))

    def get_total_cost(self):
        items = self.order_items.select_related()
        return sum(list(map(lambda x: x.quantity * x.product.price, items)))

    def delete(self):
        for item in self.order_items.select_related():
            item.product.quantity += item.quantity
            item.product.save()
        self.is_active = False
        self.save()

    @property
    def can_pay(self):
        return self.status == Order.CREATED

    @property
    def can_cancel(self):
        return self.status in [Order.CREATED, Order.PAID]


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def cost(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.product} - {self.quantity} pcs"


@receiver(pre_save, sender=OrderItem)
def product_quantity_update_on_save(sender, instance, *args, **kwargs):
    old_order_item = OrderItem.objects.filter(pk=instance.pk).first()
    if old_order_item:
        quantity_delta = instance.quantity - old_order_item.quantity
        instance.product.quantity -= quantity_delta
    else:
        instance.product.quantity -= instance.quantity
    instance.product.save()


@receiver(pre_delete, sender=OrderItem)
def product_quantity_update_on_delete(sender, instance, **kwargs):
    instance.product.quantity += instance.quantity
    instance.product.save()
