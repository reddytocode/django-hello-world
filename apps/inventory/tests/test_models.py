from django.db import IntegrityError
from django.test import TestCase

from apps.inventory.models import Product, ProductInventory, Order, ProductOrder


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

    def test_delete_product(self):
        product = Product.objects.create(name="fake_product", price=1)
        ProductInventory.objects.create(product=product, quantity=10)

        product_count = Product.objects.count()
        p_i_count = ProductInventory.objects.count()

        product.delete()
        self.assertEqual(Product.objects.count(), product_count - 1)
        self.assertEqual(ProductInventory.objects.count(), p_i_count - 1)


class ProductInventoryModelTests(TestCase):
    def test_create(self):
        product = Product.objects.create(name="fake_product", price=1)
        count = ProductInventory.objects.count()
        ProductInventory.objects.create(product=product, quantity=10)
        self.assertEqual(ProductInventory.objects.count(), count + 1)
        self.assertTrue(ProductInventory.objects.filter(product=product, quantity=10).exists())

    def test_quantity_negative(self):
        product = Product.objects.create(name="fake_product", price=1)
        wrong_quantity = -1
        with self.assertRaises(IntegrityError):
            ProductInventory.objects.create(product=product, quantity=wrong_quantity)


class OrderModelTests(TestCase):
    def test_create(self):
        order_number = "123"
        client_name = "Fake client"
        count = Order.objects.count()

        order = Order.objects.create(order_number=order_number, client_name=client_name)
        self.assertEqual(Order.objects.count(), count + 1)
        self.assertTrue(Order.objects.filter(order_number=order_number, client_name=client_name).exists())
        order.delete()

    def test_add_product(self):
        order_number = "123"
        client_name = "Fake client"
        order = Order.objects.create(order_number=order_number, client_name=client_name)
        product = Product.objects.create(name="fake_product", price=1)

        count = ProductOrder.objects.count()
        response = order.add_product(product)

        self.assertTrue(response)
        self.assertEqual(ProductOrder.objects.count(), count+1)

        self.assertTrue(ProductOrder.objects.filter(product=product, order=order).exists())

        # deberia fallar
        response = order.add_product(product)
        self.assertFalse(response)
        self.assertEqual(ProductOrder.objects.count(), count+1)

