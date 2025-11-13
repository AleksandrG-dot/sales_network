from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра пользователей."""

    class Meta:
        model = User
        fields = ["id", "username", "email", "is_active", "date_joined"]
        read_only_fields = ["date_joined"]


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для создания нового пользователя."""

    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["username", "password", "email"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data.get("email", ""),
            is_active=False,  # Пользователя активным можно сделать только другой пользователь, либо через админ-панель
        )
        return user
