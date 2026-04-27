# from rest_framework import viewsets
#
#
# class CartViewSet(viewsets.ModelViewSet):
# """
# Автосоздание корзины.
# list: возвращает список товаров в корзине, общее количество, общую сумму
# create: создает корзину
# update: добавляет / удаляет товары из корзины, изменяет количество товаров
# delete: очищает корзину
# """
#
# queryset = Product.objects.select_related("subcategory__category")
# serializer_class = ProductSerializer
# permission_classes = [
#     AllowAny,
# ]
# filter_backends = [OrderingFilter, DjangoFilterBackend, SearchFilter]
# ordering_fields = ["name", "subcategory__name", "subcategory__category__name"]
# filterset_fields = ["subcategory", "subcategory__category"]
# search_fields = [
#     "name",
# ]
# pagination_class = ProductPaginator

# def get_cart(user):
#     cart, _ = Cart.objects.get_or_create(user=user)
#     return cart
