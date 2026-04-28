from django.contrib import admin

from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    """Отображение корзины пользователей с товарами внутри и количеством на одном экране"""

    model = CartItem
    extra = 0
    readonly_fields = ("product", "quantity")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Добавляет корзины пользователей в админ-панель"""

    list_display = ("id", "user")
    inlines = [CartItemInline]
    list_filter = ("user",)
    search_fields = ("user__email",)
