from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny

from catalog.models import Category, Product
from catalog.paginators import CategoryPaginator, ProductPaginator
from catalog.serializers import CategorySerializer, ProductSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Просмотр категорий с подкатегориями.
    list: возвращает список категорий с вложенными подкатегориями и с пагинацией
    retrieve: возвращает одну категорию с подкатегориями
    """

    queryset = Category.objects.prefetch_related("subcategories")
    serializer_class = CategorySerializer
    permission_classes = [
        AllowAny,
    ]
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = [
        "name",
    ]
    search_fields = [
        "name",
    ]
    pagination_class = CategoryPaginator


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Просмотр товаров.
    list: возвращает список товаров с категорией и подкатегорией (с пагинацией)
    retrieve: возвращает детальную информацию о товаре
    """

    queryset = Product.objects.select_related("subcategory__category")
    serializer_class = ProductSerializer
    permission_classes = [
        AllowAny,
    ]
    filter_backends = [OrderingFilter, DjangoFilterBackend, SearchFilter]
    ordering_fields = ["name", "subcategory__name", "subcategory__category__name"]
    filterset_fields = ["subcategory", "subcategory__category"]
    search_fields = [
        "name",
    ]
    pagination_class = ProductPaginator
