from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Загрузка данных о пользователях из фикстур."

    def handle(self, *args, **kwargs):

        # Загружаем данные из фикстуры users_fixture.json
        call_command("loaddata", "users_fixture.json")
        self.stdout.write(self.style.SUCCESS("Успешная загрузка пользователей из фикстуры."))

        # Загружаем данные из фикстуры authtoken_fixture.json
        call_command("loaddata", "authtoken_fixture.json")
        self.stdout.write(self.style.SUCCESS("Успешная загрузка токенов аутентификации пользователей из фикстуры."))
