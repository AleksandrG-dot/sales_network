from rest_framework import serializers


def validate_debt(attrs) -> bool:
    """Валидатор проверяет на отсутствие долга перед поставщиком если не указан поставщик."""
    if attrs.get("debt") and not attrs.get("supplier"):
        raise serializers.ValidationError("Укажите поставщика перед которым долг.")
