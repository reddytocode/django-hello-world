from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, BasePermission

from apps.inventory.models import Product
from apps.inventory.serializers import ProductSerializer


class CustomPermission(BasePermission):

    def has_permission(self, request, view):
        import pdb
        pdb.set_trace()
        return True


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = (CustomPermission,)
    lookup_field = "pk"
    lookup_url_kwarg = "id"
