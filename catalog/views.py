from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny

from catalog.filters import ProductFilter
from catalog.models import Category, Product
from catalog.paginators import CategoryPaginator, ProductPaginator
from catalog.serializers import CategorySerializer, ProductSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Просмотр категорий с подкатегориями.
    list: Возвращает список категорий с вложенными подкатегориями. Доступны:
     пагинация,
     поиск названию (вхождение подстроки),
     сортировка по полю "name"
    retrieve: Возвращает категорию с подкатегориями по id категории
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
    list: Возвращает список товаров с категорией и подкатегорией (с пагинацией). Доступны:
     пагинация,
     поиск названию (вхождение подстроки),
     сортировка по полям ("name", "subcategory__name", "subcategory__category__name"),
     фильтрация по категориям через slug ("frukty", "ovoshchi", "molochnye-produkty" и др.),
     фильтрация по подкатегориям через slug ("tsitrusovye", "iagody", "korneplody", "listovye", "plodovye" и др.),
    retrieve: Возвращает детальную информацию о товаре по id товара
    """

    queryset = Product.objects.select_related("subcategory__category")
    serializer_class = ProductSerializer
    permission_classes = [
        AllowAny,
    ]
    filter_backends = [OrderingFilter, DjangoFilterBackend, SearchFilter]
    ordering_fields = ["name", "subcategory__name", "subcategory__category__name"]
    filterset_class = ProductFilter
    search_fields = [
        "name",
    ]
    pagination_class = ProductPaginator
