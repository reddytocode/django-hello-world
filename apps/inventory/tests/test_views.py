from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

from apps.inventory.models import Product
from apps.inventory.tests.factories import ProductFactory
from locallib.test_utils import BaseTest


class ProductListTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.url = reverse("inventory:product-list")
        self.app.login()
        self.products = ProductFactory.create_batch(size=2)

    def test_access(self):
        self.app.logout()
        self.app.get(self.url, status=401)

        # authenticated user
        self.app.login()
        self.app.get(self.url, status=200)

    def test_list(self):
        response = self.app.get(self.url, status=200)
        # data -> response
        # product -> DB
        for product_data, product in zip(response.data["results"], self.products):
            self.assertEqual(product_data["name"], product.name)
            self.assertEqual(product_data["price"], product.price)

    def test_num_queries(self):
        with self.assertNumQueries(3):
            self.app.get(self.url, status=200)


class ProductRetrieveTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.product = Product.objects.create(name="fake_1", price=1)
        self.url = reverse("inventory:product-retrieve", kwargs={"id": self.product.pk})
        self.app.login()

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
        self.app.login(is_super_user=True)

    def test_access(self):
        self.app.logout()
        self.app.post(self.url, data=self.data, status=401)

        # superuser user
        superuser = User.objects.create_user("superuser-1", password="1234")
        superuser.is_superuser = True
        superuser.save()
        self.app.login(superuser)
        self.app.post(self.url, data=self.data, status=201)

        # staff user hasn't access
        self.app.logout()
        staff_user = User.objects.create_user("staff-user-2", password="1234")
        staff_user.is_staff = True
        staff_user.save()
        self.app.login(staff_user)
        self.app.post(self.url, data=self.data, status=status.HTTP_403_FORBIDDEN)

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

    def test_name_can_not_have_numbers(self):
        data = {
            "name": "fake_name_123",
            "price": 12
        }

        count = Product.objects.count()

        response = self.app.post(self.url, data=data, status=400)
        self.assertEqual(response.data["name"], ["invalid name."])
        self.assertEqual(Product.objects.count(), count)


class ProductUpdateTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.product = ProductFactory()
        self.url = reverse("inventory:product-retrieve", kwargs={"id": self.product.pk})
        self.data = {
            "name": "other_name",
            "price": 2
        }
        self.app.login(is_super_user=True)

    def test_update(self):
        response = self.app.patch(self.url, data=self.data, status=200)
        self.assertEqual(response.data["name"], self.data["name"])
        self.assertEqual(response.data["price"], self.data["price"])

        self.assertFalse(Product.objects.filter(name=self.product.name, price=self.product.price).exists())
        self.assertTrue(Product.objects.filter(**self.data).exists())

    def test_unique_name(self):
        other_product = Product.objects.create(name="other_fake", price=3)
        data = {
            "name": other_product.name,
            "price": 12
        }

        response = self.app.patch(self.url, data=data, status=400)
        self.assertEqual(response.data["name"], ["product with this name already exists."])


class ProductDeleteTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.product = ProductFactory()
        self.url = reverse("inventory:product-retrieve", kwargs={"id": self.product.pk})
        self.app.login(is_super_user=True)

    def test_delete(self):
        count = Product.objects.count()

        self.app.delete(self.url, status=204)
        self.assertEqual(Product.objects.count(), count-1)

        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())

    def test_product_does_not_exists(self):
        url = reverse("inventory:product-retrieve", kwargs={"id": 123})
        self.app.delete(url, status=404)