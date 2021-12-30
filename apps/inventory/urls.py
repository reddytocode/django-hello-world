from django.urls import path

from apps.inventory.views import ProductViewSet


app_name = "inventory"

urlpatterns = [
    path('products/', ProductViewSet.as_view({"get": "list", "post": "create"}), name="product-list"),
    path('products/<id>', ProductViewSet.as_view({"get": "retrieve", "patch": "partial_update", "delete": "destroy"}), name="product-retrieve"),
]
