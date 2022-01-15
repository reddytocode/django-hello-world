from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.inventory.models import Product
from apps.inventory.serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = (IsAuthenticated,)
    lookup_field = "pk"
    lookup_url_kwarg = "id"
