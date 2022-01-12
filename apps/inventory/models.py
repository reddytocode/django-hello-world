from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.IntegerField()

    def __str__(self):
        return f"Product {self.name}, {self.price}$"


class ProductInventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="inventory")
    quantity = models.PositiveIntegerField(validators=(MinValueValidator(0), ))


class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_orders")
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="product_orders")


class Order(models.Model):
    order_number = models.IntegerField(unique=True)
    client_name = models.CharField(max_length=100)
    products = models.ManyToManyField(Product, through=ProductOrder, related_name="orders")

    def add_product(self, product) -> bool:
        if product in list(self.products.all()):
            return False
        self.products.add(product)
        return True