from rest_framework import viewsets
from apps.inventory.models import Product
from apps.inventory.serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()