from django.urls import path

from apps.inventory.views import ProductViewSet


app_name = "inventory"

urlpatterns = [
    path('products/', ProductViewSet.as_view({"get": "list"}), name="product-list"),
]