from django.contrib import admin
from apps.inventory.models import Product, ProductInventory, ProductOrder, Order


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductInventory)
class ProductInventoryAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductOrder)
class ProductOrderAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass