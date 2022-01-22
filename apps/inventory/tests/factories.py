import factory
from apps.inventory.models import Product, ProductInventory


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
    name = factory.Sequence(lambda n: f"product-{n}")
    price = factory.Faker("pyint", min_value=0, max_value=100)


class ProductInventoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductInventory
    product = factory.SubFactory(ProductFactory)
    quantity = factory.Faker("pyint", min_value=0, max_value=100)

# TODO: CREATE factory for Product Order and Order
# order
# name = factory.Faker("name")
# no se necesita el product
