from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ContactViewSet, NetworkNodeViewSet, ProductViewSet

router = DefaultRouter()
router.register(r"network-nodes", NetworkNodeViewSet, basename="networknode")
router.register(r"contacts", ContactViewSet, basename="contact")
router.register(r"products", ProductViewSet, basename="product")


urlpatterns = [
    path("", include(router.urls)),
]
