from rest_framework import serializers

from .models import Category, Product, SubCategory


class SubCategorySerializer(serializers.ModelSerializer):
    """Сериализатор подкатегории"""

    category = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = SubCategory
        fields = ("id", "name", "category", "slug", "image")


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категории с подкатегориями"""

    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ("id", "name", "slug", "image", "subcategories")


class CategoryMiniSerializer(serializers.ModelSerializer):
    """Упрощенный сериализатор категории: для отображения краткой информации"""

    class Meta:
        model = Category
        fields = ("id", "name", "slug")


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор товара"""

    image = serializers.SerializerMethodField()
    category = CategoryMiniSerializer(source="subcategory.category", read_only=True)
    subcategory = serializers.CharField(source="subcategory.name", read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "slug",
            "category",
            "subcategory",
            "price",
            "image",
        )

    def _build_url(self, request, field):
        """Генерирует абсолютный url на основе текущего запроса"""
        url = getattr(field, "url", None)
        return request.build_absolute_uri(url) if request else url

    def get_image(self, obj):
        """
        Генерирует изображение в 3 разных размерах и агрегирует их в одном поле image
        (без сохранения в базе данных)
        """
        request = self.context.get("request")
        return {
            "original": self._build_url(request, obj.image),
            "small": self._build_url(request, obj.image_small),
            "medium": self._build_url(request, obj.image_medium),
            "large": self._build_url(request, obj.image_large),
        }


class ProductCreateSerializer(serializers.ModelSerializer):
    """Создание товара"""

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be positive")
        return value

    class Meta:
        model = Product
        fields = ("name", "price", "subcategory", "image")
        read_only_fields = ("slug",)


class ProductUpdateSerializer(serializers.ModelSerializer):
    """Обновление товара"""

    class Meta:
        model = Product
        fields = ("name", "price", "subcategory", "image")
        read_only_fields = ("slug",)
