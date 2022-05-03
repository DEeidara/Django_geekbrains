from django.core.management.base import BaseCommand
from mainapp.models import Category, Product
from authapp.models import ShopUser
from django.conf import settings
from django.db import IntegrityError
import json
import os


def load_from_json(filename):
    with open(os.path.join(settings.JSON_ROOT, filename + '.json'), 'r') as f:
        return json.load(f)


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        categories = load_from_json('categories')

        Category.objects.all().delete()
        for category in categories:
            try:
                Category.objects.create(**category)
            except IntegrityError:
                pass

        products = load_from_json('products')

        Product.objects.all().delete()
        for product in products:
            product['category'] = Category.objects.get(
                name=product['category'])
            Product.objects.create(**product)

        if not ShopUser.objects.filter(username='admin'):
            ShopUser.objects.create_superuser(
                username='admin', email='admin@localhost', password='adminadmin')
