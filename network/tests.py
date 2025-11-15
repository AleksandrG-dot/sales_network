from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Contact, NetworkNode, Product

User = get_user_model()


class NetworkNodeTestCase(APITestCase):
    """Тест-кейс для модели NetworkNode"""

    def setUp(self):
        """Подготовка данных для тестов"""
        self.user = User.objects.create_user(
            username="testuser", password="testpass123", email="test@example.com", is_active=True
        )

        # Создаем тестовые данные
        self.contact1 = Contact.objects.create(
            email="factory@example.com", country="RU", city="Moscow", street="Lenina", house="1"
        )

        self.contact2 = Contact.objects.create(
            email="retail@example.com", country="RU", city="SPb", street="Nevsky", house="2"
        )

        self.product1 = Product.objects.create(name="Smartphone", model="X100", release_date="2023-01-01")

        self.product2 = Product.objects.create(name="Tablet", model="T200", release_date="2023-02-01")

        # Создаем завод (уровень 0)
        self.factory = NetworkNode.objects.create(
            name="Factory A",
            type="factory",
        )
        self.factory.contacts.add(self.contact1)

        # Создаем розничную сеть (уровень 1)
        self.retail = NetworkNode.objects.create(name="Retail B", type="retail", supplier=self.factory, debt=5000.00)
        # Добавляем данный с полями ManyToMany
        self.retail.contacts.add(self.contact2)
        self.retail.products.add(self.product1, self.product2)

        # URL для тестов
        self.list_url = reverse("networknode-list")
        self.detail_url = reverse("networknode-detail", kwargs={"pk": self.retail.pk})

    def authenticate(self):
        """Аутентификация пользователя"""
        self.client.force_authenticate(user=self.user)

    def test_network_node_list_unauthenticated(self):
        """Тест получения списка звеньев сети (неаутентифицированный пользователь)."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_network_node_list_authenticated(self):
        """Тест получения списка звеньев сети (аутентифицированный пользователь)."""
        self.authenticate()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_network_node_create(self):
        """Тест создания нового звена сети."""
        self.authenticate()

        new_contact = Contact.objects.create(
            email="new@example.com", country="CN", city="Beijing", street="Main", house="10"
        )

        data = {
            "name": "New Retail",
            "type": "retail",
            "contacts": [new_contact.id],
            "supplier": self.factory.id,
            "products": [self.product1.id],
            "debt": "0.00",
        }

        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(NetworkNode.objects.all().count(), 3)

    def test_network_node_update_debt_protection(self):
        """Тест защиты от обновления поля debt."""
        self.authenticate()

        data = {"name": "Updated Retail", "debt": "0.00"}

        response = self.client.patch(self.detail_url, data, format="json")
        updated_retail = NetworkNode.objects.get(pk=self.retail.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_retail.name, "Updated Retail")
        self.assertNotEqual(updated_retail.debt, Decimal("0.00"))

    def test_network_node_delete(self):
        """Тест удаления звена сети."""
        self.authenticate()

        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(NetworkNode.objects.all().count(), 1)
        self.assertEqual(Product.objects.all().count(), 2)
        self.assertEqual(Contact.objects.all().count(), 2)

    def test_network_node_filter_by_country(self):
        """Тест фильтрации по стране."""
        self.authenticate()

        response = self.client.get(f"{self.list_url}?contact__country=RU")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_network_node_level_calculation(self):
        """Тест автоматического расчета уровня иерархии."""
        self.assertEqual(self.factory.level, 0)
        self.assertEqual(self.retail.level, 1)


class ProductTestCase(APITestCase):
    """Тест-кейс для модели Product."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123", is_active=True)

        self.product = Product.objects.create(name="Laptop", model="L500", release_date="2023-03-01")

        self.list_url = reverse("product-list")
        self.detail_url = reverse("product-detail", kwargs={"pk": self.product.pk})

    def authenticate(self):
        self.client.force_authenticate(user=self.user)

    def test_product_list_unauthenticated(self):
        """Тест получения списка продуктов (неаутентифицированный пользователь)."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_product_list_authenticated(self):
        """Тест получения списка продуктов (аутентифицированный пользователь)."""
        self.authenticate()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_product_create(self):
        """Тест создания нового продукта."""
        self.authenticate()

        data = {"name": "New Product", "model": "X8080", "release_date": "2025-11-15"}

        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.all().count(), 2)

    def test_product_delete(self):
        """Тест удаления продукта."""
        self.authenticate()

        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.all().count(), 0)

    def test_product_search(self):
        """Тест поиска продуктов"""
        self.authenticate()

        response = self.client.get(f"{self.list_url}?search=Laptop")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class ContactTestCase(APITestCase):
    """Тест-кейс для модели Contact"""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123", is_active=True)

        self.contact = Contact.objects.create(
            email="contact@example.com", country="US", city="New York", street="Broadway", house="100"
        )

        self.list_url = reverse("contact-list")
        self.detail_url = reverse("contact-detail", kwargs={"pk": self.contact.pk})

    def authenticate(self):
        self.client.force_authenticate(user=self.user)

    def test_contact_list_unauthenticated(self):
        """Тест получения списка контактов (неаутентифицированный пользователь)."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_contact_list_authenticated(self):
        """Тест получения списка контактов (аутентифицированный пользователь)."""
        self.authenticate()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_contact_create(self):
        """Тест создания нового контакта."""
        self.authenticate()

        data = {
            "email": "contact2@example.com",
            "country": "RU",
            "city": "Новгород",
            "street": "Первомайская",
            "house": "2",
        }

        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contact.objects.all().count(), 2)

    def test_contact_delete(self):
        """Тест удаления контактов."""
        self.authenticate()

        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.all().count(), 0)

    def test_contact_search(self):
        """Тест поиска контактов."""
        self.authenticate()

        response = self.client.get(f"{self.list_url}?search=New York")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
