from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from apps.inventory.models import Product
from apps.inventory.permissions import IsSuperUser
from apps.inventory.serializers import ProductSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Product List",
        description="Returns Paginated list of products.",
    ),
)
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"
    lookup_url_kwarg = "id"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.order_by("-price")

    def get_permissions(self):
        if self.action not in ("list", "retrieve"):
            self.permission_classes = self.permission_classes + [IsSuperUser]
        return super().get_permissions()
