import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        password = os.getenv("SUPERUSER_PASS")
        user_model = get_user_model()
        user = user_model.objects.create(username=os.getenv("SUPERUSER_USERNAME"), email=os.getenv("SUPERUSER_EMAIL"))
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.stdout.write(
            self.style.SUCCESS(f"Успешное создание суперпользователя '{user.username}' с паролем: {password}")
        )
