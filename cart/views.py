from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Cart, CartItem
from .serializers import (
    CartItemCreateUpdateSerializer,
    CartSerializer,
)


class CartViewSet(viewsets.ViewSet):
    """
    Автосоздание корзины.
    list: возвращает список товаров в корзине, общее количество, общую сумму
    create: создает корзину
    update: добавляет / удаляет товары из корзины, изменяет количество товаров
    delete: очищает корзину
    """

    permission_classes = [
        IsAuthenticated,
    ]

    def get_cart(self, request):
        """Автосоздание корзины для товаров"""
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart

    def list(self, request):
        """Возвращает список товаров в корзине"""
        cart = Cart.objects.prefetch_related("items__product").get(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def add(self, request):
        """
        Добавляет товар в корзину.
        Если товар уже в корзине, обновляет количество
        """
        cart = self.get_cart(request)
        serializer = CartItemCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data["product"]
        quantity = serializer.validated_data["quantity"]
        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
        )
        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity
        item.save()
        return Response({"detail": "Товар добавлен в корзину"}, status=201)

    @action(detail=False, methods=["patch"])
    def update_item(self, request):
        """Обновляет количество товара в корзине"""
        cart = self.get_cart(request)
        serializer = CartItemCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quantity = serializer.validated_data["quantity"]
        product = serializer.validated_data["product"]
        try:
            item = CartItem.objects.get(cart=cart, product_id=product.id)
        except CartItem.DoesNotExist:
            return Response({"detail": "Товар не найден"}, status=404)

        item.quantity = quantity
        item.save()
        return Response({"detail": "Количество обновлено"}, status=200)

    @action(detail=False, methods=["delete"])
    def remove(self, request):
        """Удаляет товар из корзины"""
        cart = self.get_cart(request)
        serializer = CartItemCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data["product"]
        deleted, _ = CartItem.objects.filter(cart=cart, product=product).delete()
        if not deleted:
            return Response({"detail": "Товар не найден"}, status=404)
        return Response({"detail": "Товар удален"}, status=204)

    @action(detail=False, methods=["delete"])
    def clear(self, request):
        """Очищает корзину"""
        cart = self.get_cart(request)
        cart.items.all().delete()
        return Response({"detail": "Корзина очищена"}, status=204)
