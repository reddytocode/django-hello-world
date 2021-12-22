from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.IntegerField()

    def __str__(self):
        return f"Product {self.name}, {self.price}$"