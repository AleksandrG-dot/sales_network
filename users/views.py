from django.contrib.auth.models import User
from rest_framework import permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from users.serializers import UserRegistrationSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet для создания новых пользователей."""

    queryset = User.objects.all()

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "create":
            return UserRegistrationSerializer
        return UserSerializer

    def create(self, request):
        """Регистрация нового пользователя (выдается токен пользователя)."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {"token": token.key, "user_id": user.id, "username": user.username}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
