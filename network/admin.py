from django.contrib import admin
from .models import Product, Contact, NetworkNode


class CityFilter(admin.SimpleListFilter):
    """Кастомный фильтр по городам."""

    title = "Город"
    parameter_name = "city"

    def lookups(self, request, model_admin):
        cities = Contact.objects.values_list("city", flat=True).distinct().order_by("city")
        return [(city, city) for city in cities if city]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(contact__city=self.value())
        return queryset


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "model",
        "release_date",
    )


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "country",
        "city",
        "street",
        "house",
    )


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "type",
        "level",
        "debt",
        "created_at",
    )
    list_filter = (CityFilter,)
    actions = ("clear_debt",)

    def clear_debt(self, request, queryset):
        """Admin action для очистки задолженностей."""
        queryset.update(debt=0)

    clear_debt.short_description = "Очистить задолженность"
