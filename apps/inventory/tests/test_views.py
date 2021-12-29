from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse

from apps.inventory.models import Product


class CustomAPIClient():
    def __init__(self, test_case):
        self.app = APIClient()
        self.test_case = test_case

    def get(self, url, data=None, status=None):
        response = self.app.get(url, data=data)
        if status is None:
            self.test_case.assertEqual(response.status_code, status)
        return response

    def post(self, url, data=None, status=None):
        response = self.app.post(url, data=data)
        if status is None:
            self.test_case.assertEqual(response.status_code, status)
        return response


class BaseTest(TestCase):
    def setUp(self):
        self.app = CustomAPIClient(self)


class ProductListTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.url = reverse("inventory:product-list")

    def test_list(self):
        self.app.get(self.url, status=200)


class ProductRetrieveTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.product = Product.objects.create(name="fake_1", price=1)
        self.url = reverse("inventory:product-retrieve", kwargs={"id": self.product.pk})

    def test_ok(self):
        response = self.app.get(self.url, status=200)
        self.assertEqual(response.data["name"], self.product.name)
        self.assertEqual(response.data["price"], self.product.price)


class ProductCreateTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.url = reverse("inventory:product-list")
        self.data = {
            "name": "fake_name",
            "price": 12
        }

    def test_create(self):
        count = Product.objects.count()
        response = self.app.post(self.url, data=self.data, status=201)
        self.assertEqual(Product.objects.count(), count + 1)

        self.assertEqual(response.data["name"], self.data["name"])
        self.assertEqual(response.data["price"], self.data["price"])

        self.assertTrue(Product.objects.filter(**self.data).exists())

    def test_create_repeated_name_should_fail(self):
        product = Product.objects.create(name="fake", price=10)
        self.data["name"] = product.name

        count = Product.objects.count()

        response = self.app.post(self.url, data=self.data, status=400)
        self.assertEqual(response.data["name"], ["product with this name already exists."])

        self.assertEqual(Product.objects.count(), count)
