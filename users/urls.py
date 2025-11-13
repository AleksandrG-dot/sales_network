from django.urls import include, path
from rest_framework.authtoken import views as auth_views
from rest_framework.routers import DefaultRouter

from .views import UserViewSet

router = DefaultRouter()
router.register(r"user", UserViewSet, basename="user")

urlpatterns = [
    path("login/", auth_views.obtain_auth_token),  # Получение токена
    path("", include(router.urls)),
]
