from django.contrib.auth.models import User
from django.urls import reverse
from apps.inventory.models import Product
from locallib.test_utils import BaseTest


class ProductListTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.url = reverse("inventory:product-list")
        self.app.login()

    def test_access(self):
        self.app.logout()
        self.app.get(self.url, status=401)

        # authenticated user
        self.app.login()
        self.app.get(self.url, status=200)

    def test_list(self):
        user = User.objects.create_user("Asdf", password="1234dff")
        response = self.app.post(reverse("users:token_obtain_pair"), {"username": user.username, "password": "1234dff"})
        access_token = response.data["access"]
        print("access", access_token)
        self.app.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
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
        self.app.login()

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
        self.product = Product.objects.create(name="fake_1", price=1)
        self.url = reverse("inventory:product-retrieve", kwargs={"id": self.product.pk})
        self.data = {
            "name": "other_name",
            "price": 2
        }
        self.app.login()

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
        self.product = Product.objects.create(name="fake_1", price=1)
        self.url = reverse("inventory:product-retrieve", kwargs={"id": self.product.pk})
        self.app.login()

    def test_delete(self):
        count = Product.objects.count()
        self.app.delete(self.url, status=204)
        self.assertEqual(Product.objects.count(), count-1)

        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())

    def test_product_does_not_exists(self):
        url = reverse("inventory:product-retrieve", kwargs={"id": 123})
        self.app.delete(url, status=404)
