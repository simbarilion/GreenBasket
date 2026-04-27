from django.contrib import admin

from catalog.models import Category, Product, SubCategory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Добавляет категории в админ-панель"""

    model = Category
    list_display = (
        "name",
        "slug",
        "image",
        "created_at",
        "updated_at",
    )
    search_fields = ("name", "slug")


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    """Добавляет подкатегории в админ-панель"""

    model = SubCategory
    list_display = (
        "name",
        "slug",
        "category",
        "image",
        "created_at",
        "updated_at",
    )
    search_fields = ("name", "slug")
    list_filter = ("category",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Добавляет товары в админ-панель"""

    model = Product
    list_display = (
        "name",
        "slug",
        "subcategory",
        "price",
        "image",
        "created_at",
        "updated_at",
    )
    search_fields = ("name", "slug")
    list_filter = ("subcategory",)
