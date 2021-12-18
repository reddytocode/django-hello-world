from django.db import IntegrityError
from django.test import TestCase

from apps.inventory.models import Product


class ProductModelTests(TestCase):
    def test_create(self):
        count = Product.objects.count()

        product = Product.objects.create(name="fake_product", price=1)

        self.assertEqual(Product.objects.count(), count+1)
        self.assertTrue(Product.objects.filter(name="fake_product", price=1).exists())
        product.delete()

    def test_unique_name(self):
        name = "fake_product_2"

        count = Product.objects.count()
        Product.objects.create(name=name, price=1)
        self.assertEqual(Product.objects.count(), count + 1)

        with self.assertRaises(IntegrityError):
            Product.objects.create(name=name, price=4)
