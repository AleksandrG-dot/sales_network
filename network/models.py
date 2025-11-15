from django.db import models
from django_countries.fields import CountryField

from config.settings import NODE_TYPES


class Product(models.Model):
    """Модель с продуктами."""

    name = models.CharField(max_length=150, verbose_name="Название", help_text="Введите название продукта")
    model = models.CharField(
        max_length=200, verbose_name="Модель", help_text="Введите модель продукта", null=True, blank=True
    )
    release_date = models.DateField(
        verbose_name="Дата выхода на рынок", help_text="Введите дату выхода на рынок", null=True, blank=True
    )

    def __str__(self):
        return f"{self.name} ({self.model})" if self.model else self.name

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "Продукты"


class Contact(models.Model):
    """Модель с контактными данными."""

    email = models.EmailField(verbose_name="E-mail", help_text="Введите e-mail")
    country = CountryField(default="ru", blank_label="Выберите страну")
    city = models.CharField(max_length=150, verbose_name="Город", help_text="Введите город")
    street = models.CharField(max_length=150, verbose_name="Улица", help_text="Введите улицу")
    house = models.CharField(max_length=10, verbose_name="Номер дома", help_text="Введите номер дома")

    def __str__(self):
        return f"{self.email} {self.country}, {self.city}, {self.street}, {self.house}"

    class Meta:
        verbose_name = "контакт"
        verbose_name_plural = "Контакты"


class NetworkNode(models.Model):
    """Модель со звеньями сети по продаже электроники."""

    name = models.CharField(max_length=150, verbose_name="Название", help_text="Введите название звена сети")
    # Тип звена сети по иерархии
    type = models.CharField(
        max_length=15, choices=NODE_TYPES, verbose_name="Тип звена", help_text="Выберите тип звена сети"
    )

    contacts = models.ManyToManyField(
        Contact, verbose_name="Контакты", help_text="Выберите контакты для этого звена сети"
    )

    products = models.ManyToManyField(
        Product, verbose_name="Продукт", help_text="Выберите продукты, которые реализует это звено"
    )

    supplier = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Поставщик",
        help_text="Выберите поставщика оборудования",
        related_name="child",
    )
    # Уровень в иерархии
    # Не редактируемо вручную, вычисляется автоматически (переопределен save())
    level = models.PositiveIntegerField(editable=False, verbose_name="Уровень в иерархии")

    debt = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Задолженность перед поставщиком",
        help_text="Введите задолженность перед поставщиком в рублях",
        default=0.00,
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    def save(self, *args, **kwargs):
        """Переопределение save для автоматического вычисления уровня."""
        if self.supplier is None:  # Если не указан поставщик, то считаю что это завод (с уровнем 0)
            self.level = 0
        else:
            self.level = self.supplier.level + 1  # noqa
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_type_display()}: {self.name} (Уровень {self.level})"  # noqa

    class Meta:
        verbose_name = "звено сети"
        verbose_name_plural = "Звенья сети"
