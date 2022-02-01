from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from apps.inventory.models import Product
from apps.inventory.permissions import IsSuperUser
from apps.inventory.serializers import ProductSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Products List",
        description="Returns Paginated list of products.",
    ),
    create=extend_schema(
        summary="Product Create",
        description="Returns a form to create a product.",
    ),
    retrieve=extend_schema(
        summary="Product Retrieve",
        description="Returns a certain Product",
    ),
    partial_update=extend_schema(
        summary="Product Partial Update",
        description="Returns a form to update a certain Product",
    ),
    destroy=extend_schema(
        summary="Product Delete",
        description="Returns a page to delete a product",
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
