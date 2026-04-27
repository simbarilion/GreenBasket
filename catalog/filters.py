import django_filters

from catalog.models import Product


class ProductFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name="subcategory__category__slug")
    subcategory = django_filters.CharFilter(field_name="subcategory__slug")

    class Meta:
        model = Product
        fields = ["category", "subcategory"]
