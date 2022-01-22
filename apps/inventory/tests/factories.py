import factory

from apps.inventory.models import Product


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
    name = factory.Sequence(lambda n: f"product-{n}")
    price = factory.Sequence(lambda n: n)

