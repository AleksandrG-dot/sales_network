from rest_framework import serializers

from .models import Contact, NetworkNode, Product
from .validators import validate_debt


class ContactSerializer(serializers.ModelSerializer):
    """Сериализатор для контактов"""

    class Meta:
        model = Contact
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для продуктов"""

    class Meta:
        model = Product
        fields = "__all__"


class NetworkNodeReadSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра звена сети."""

    contacts = ContactSerializer(many=True, read_only=True)
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = NetworkNode
        fields = ("id", "name", "type", "level", "contacts", "products", "supplier", "debt", "created_at")
        read_only_fields = ("level", "created_at")
        validators = (validate_debt,)


class NetworkNodeWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для записи звена сети."""

    class Meta:
        model = NetworkNode
        fields = ["id", "name", "type", "level", "contacts", "products", "supplier", "debt", "created_at"]
        read_only_fields = ["level", "created_at"]
        validators = (validate_debt,)

    def update(self, instance, validated_data):
        """Запрещаем обновление поля debt через API"""
        if "debt" in validated_data:
            # Удаляем debt из данных для обновления
            validated_data.pop("debt")
        return super().update(instance, validated_data)
