from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Добавляет пользователей в админ-панель"""

    model = CustomUser
    list_display = (
        "email",
        "is_active",
        "is_verified",
        "is_staff",
        "is_superuser",
    )
    list_editable = ("is_verified", "is_active")
    list_filter = ("is_active", "is_verified", "is_staff")
    search_fields = ("email", "phone_number", "city")

    fieldsets = UserAdmin.fieldsets + (
        (
            "Дополнительная информация",
            {"fields": ("phone_number", "city", "is_verified")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "phone_number", "city", "is_active", "is_verified"),
            },
        ),
    )
