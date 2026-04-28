from django.contrib import admin
from django.utils.html import format_html

from catalog.models import Category, Product, SubCategory


class ImagePreviewMixin:
    image_field = "image"

    @admin.display(description="Image")
    def image_preview(self, obj):
        image = getattr(obj, self.image_field, None)
        if image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', image.url)
        return "-"


@admin.register(Category)
class CategoryAdmin(ImagePreviewMixin, admin.ModelAdmin):
    """Добавляет категории в админ-панель"""

    model = Category
    list_display = (
        "slug",
        "name",
        "image_preview",
        "created_at",
        "updated_at",
    )
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("name",)


@admin.register(SubCategory)
class SubCategoryAdmin(ImagePreviewMixin, admin.ModelAdmin):
    """Добавляет подкатегории в админ-панель"""

    model = SubCategory
    list_display = (
        "slug",
        "name",
        "category",
        "image",
        "created_at",
        "updated_at",
    )
    search_fields = ("name", "slug")
    list_filter = ("category",)
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("name", "category")


@admin.register(Product)
class ProductAdmin(ImagePreviewMixin, admin.ModelAdmin):
    """Добавляет товары в админ-панель"""

    model = Product
    list_display = (
        "slug",
        "name",
        "subcategory",
        "price",
        "image",
        "created_at",
        "updated_at",
    )
    search_fields = ("name", "slug")
    list_filter = ("subcategory",)
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("name", "price", "subcategory")
