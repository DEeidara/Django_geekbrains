from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=40, unique=True)
    description = models.TextField(max_length=255)

    def __str__(self):
        return f'{self.id}: {self.name}'


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=40, unique=True)
    description = models.TextField(max_length=255, blank=True)
    image = models.ImageField(upload_to='product_images', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.id}: {self.name}'
