from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html, format_html_join

from .models import Contact, NetworkNode, Product


class CityFilter(admin.SimpleListFilter):
    """Кастомный фильтр по городам."""

    title = "Город"
    parameter_name = "city"

    def lookups(self, request, model_admin):
        cities = Contact.objects.values_list("city", flat=True).distinct().order_by("city")
        return [(city, city) for city in cities if city]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(contacts__city=self.value())
        return queryset


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "model", "release_date")
    list_filter = ("release_date",)
    search_fields = ("name", "model")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("email", "country", "city", "street", "house")
    list_filter = ("country", "city")
    search_fields = ("email",)


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "type",
        "level",
        "contacts_link",
        "count_products",
        "supplier_link",
        "debt",
        "created_at",
    )
    readonly_fields = ("created_at", "level")
    list_filter = (CityFilter, "type", "created_at")
    actions = ("clear_debt",)
    search_fields = ("name", "contacts__email")

    @admin.action(description="Кол-во прод.")
    def count_products(self, obj):
        """Поле с количеством продуктов у звена сети."""
        return obj.products.count()

    @admin.action(description="Контакты")
    def contacts_link(self, obj):
        con_list = obj.contacts.values_list("id", "email")
        return format_html_join(
            "",
            "<p style='margin: 0; padding: 0;'><a href='{}'>{}</a></p>",
            ((reverse("admin:network_contact_change", args=[item[0]]), item[1]) for item in con_list),
        )

    @admin.action(description="Поставщик")
    def supplier_link(self, obj):
        if obj.supplier:
            url = reverse("admin:network_networknode_change", args=[obj.supplier.id])
            return format_html("<a href='{}'>{}</a>", url, obj.supplier.name)
        return "—"

    def clear_debt(self, request, queryset):
        """Admin action для очистки задолженностей."""
        updated_count = queryset.update(debt=0)
        self.message_user(request, f"Задолженность очищена у {updated_count} объектов")

    clear_debt.short_description = "Очистить задолженность"
