import factory
from apps.inventory.models import Product, ProductInventory, Order, ProductOrder


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


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    order_number = factory.Sequence(lambda n: n)
    client_name = factory.Faker("name")


class ProductOrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductOrder

    product = factory.SubFactory(ProductFactory)
    order = factory.SubFactory(OrderFactory)
