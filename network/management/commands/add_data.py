from django.core.management import call_command
from django.core.management.base import BaseCommand

from network.models import Contact, NetworkNode, Product


class Command(BaseCommand):
    help = "Загрузка данных о продуктах, контактах и узлах сети из фикстур."

    def handle(self, *args, **kwargs):
        # Удаляем существующие записи
        NetworkNode.objects.all().delete()
        Product.objects.all().delete()
        Contact.objects.all().delete()

        # Загружаем данные из фикстуры network_fixture.json
        call_command("loaddata", "network_fixture.json")
        self.stdout.write(
            self.style.SUCCESS("Успешно загружены данные о продуктах, контактах и узлах сети из фикстур.")
        )
