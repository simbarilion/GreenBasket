from rest_framework.pagination import PageNumberPagination


class ProductPaginator(PageNumberPagination):
    """Настраивает пагинацию для списка товаров в корзине (по 20 на странице)"""

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 30
