from django.db import models

from catalog.models import Product
from users.models import CustomUser


class Cart(models.Model):
    """Модель корзины для товаров"""

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="cart")

    def __str__(self):
        """Строковое представление корзины пользователя"""
        return f"Cart ({self.user.email})"


class CartItem(models.Model):
    """Модель товара в корзине пользователя"""

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        """Строковое представление товара в корзине пользователя"""
        return f"{self.product.name} x {self.quantity}"

    class Meta:
        unique_together = ("cart", "product")
