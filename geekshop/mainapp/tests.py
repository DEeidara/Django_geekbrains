from urllib import response
from django.test import TestCase

from mainapp.models import Category, Product


class MainappSmokeTest(TestCase):
    def setUp(self):
        category = Category.objects.create(name="cat1")
        for i in range(10):
            Product.objects.create(
                category=category,
                name=f"prod{i}",
                description="qwe",
                price=1000,
                image="default.jpg",
            )

    def test_categories_urls(self):
        for cat in Category.objects.all():
            response = self.client.get(f"/products/{cat.pk}/")
            self.assertEqual(response.status_code, 200)

    def test_products_urls(self):
        for prod in Product.objects.all():
            response = self.client.get(f"/products/product/{prod.pk}/")
            self.assertEqual(response.status_code, 200)

    def test_mainapp_urls(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    # after test has ended
    # def tearDown(self):
    #     pass
