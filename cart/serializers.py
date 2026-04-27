from rest_framework import serializers

from cart.models import Cart, CartItem
from catalog.serializers import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    """Сериализатор товара в корзине пользователя"""

    product = ProductSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ("id", "product", "quantity", "total_price")

    def get_total_price(self, obj):
        return obj.quantity * obj.product.price


class CartItemCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор добавления / изменения (количества) товара в корзине пользователя"""

    class Meta:
        model = CartItem
        fields = ("product", "quantity")

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Количество должно быть больше 0")
        return value


class CartSerializer(serializers.ModelSerializer):
    """Сериализатор корзины для товаров пользователя"""

    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    total_quantity = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ("id", "items", "total_quantity", "total_price")

    def get_total_price(self, obj):
        return sum(item.product.price * item.quantity for item in obj.items.all())

    def get_total_quantity(self, obj):
        return sum(item.quantity for item in obj.items.all())
