from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Класс для настройки админ-панели"""

    model = CustomUser
    list_display = (
        "email",
        "username",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    fieldsets = UserAdmin.fieldsets + (
        (
            "Дополнительная информация",
            {"fields": ("phone_number", "city")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                    "phone_number",
                    "city",
                    "is_active",
                ),
            },
        ),
    )
