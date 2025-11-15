from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from users.permissions import IsActiveEmployee

from .models import Contact, NetworkNode, Product
from .serializers import ContactSerializer, NetworkNodeReadSerializer, NetworkNodeWriteSerializer, ProductSerializer


class ContactViewSet(viewsets.ModelViewSet):
    """ViewSet для CRUD операций с контактами."""

    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsActiveEmployee]
    filter_backends = [filters.SearchFilter]
    search_fields = ("country", "city", "email")


class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet для CRUD операций с продуктами."""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsActiveEmployee]
    filter_backends = [filters.SearchFilter]
    search_fields = ("name", "model")


class NetworkNodeViewSet(viewsets.ModelViewSet):
    """ViewSet для CRUD операций со звеньями сети."""

    # Без distinct() в случае если у узла сети несколько контактов,
    # то вывод этого узла увеличивается на количество контактов.
    queryset = NetworkNode.objects.all().distinct()
    permission_classes = [IsActiveEmployee]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("contacts__country",)
    ordering_fields = ("id", "name", "level", "debt", "created_at")

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return NetworkNodeWriteSerializer
        return NetworkNodeReadSerializer
