from rest_framework import permissions


class IsActiveEmployee(permissions.BasePermission):
    """
    Разрешает доступ только активным сотрудникам.
    ПРИМЕЧАНИЕ: Django и DRF по умолчанию уже блокируют неактивных пользователей,
    но это явно требовалось в задании.
    """

    message = "Пользователь не is_active"

    def has_permission(self, request, view):
        return request.user.is_active
