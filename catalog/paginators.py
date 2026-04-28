from rest_framework.pagination import PageNumberPagination


class CategoryPaginator(PageNumberPagination):
    """Настраивает пагинацию для списка категорий с подкатегориями (по 6 на странице)"""

    page_size = 6
    page_size_query_param = "page_size"
    max_page_size = 12


class ProductPaginator(PageNumberPagination):
    """Настраивает пагинацию для списка товаров с категориями и подкатегориями (по 12 на странице)"""

    page_size = 12
    page_size_query_param = "page_size"
    max_page_size = 18
