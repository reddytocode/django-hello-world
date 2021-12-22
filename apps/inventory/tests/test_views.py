from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse

from apps.inventory.models import Product


class ProductListTests(TestCase):
    def setUp(self):
        self.app = APIClient()
        self.url = reverse("inventory:product-list")

    def test_list(self):
        response = self.app.get(self.url)
        self.assertEqual(response.status_code, 200)
        # todo: verify product info is in the response


class ProductCreateTests(TestCase):
    def setUp(self):
        self.app = APIClient()
        self.url = reverse("inventory:product-list")
        self.data = {
            "name": "fake_name",
            "price": 12
        }

    def test_create(self):
        count = Product.objects.count()
        response = self.app.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.objects.count(), count + 1)

        self.assertEqual(response.data["name"], self.data["name"])
        self.assertEqual(response.data["price"], self.data["price"])

        self.assertTrue(Product.objects.filter(**self.data).exists())

    def test_create_repeated_name_should_fail(self):
        product = Product.objects.create(name="fake", price=10)
        self.data["name"] = product.name

        count = Product.objects.count()

        response = self.app.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 400)

        self.assertEqual(Product.objects.count(), count)



