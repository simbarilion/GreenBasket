import uuid

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from catalog.validators import validate_image


class SlugMixin(models.Model):
    """Универсальная модель-миксин для создания slug"""

    slug = models.SlugField(unique=True, db_index=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f"{slugify(self.name)}-{uuid.uuid4().hex[:6]}"
        super().save(*args, **kwargs)


class Category(SlugMixin):
    """
    Модель категории товаров.
    Может содержать подкатегории товаров и товары.
    Использует slug
    """

    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="categories/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name", ""]


class SubCategory(SlugMixin):
    """
    Модель подкатегории товаров.
    Связана с категорией товаров. Может содержать товары.
    Использует slug
    """

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="subcategories/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        ordering = ["name"]


class Product(SlugMixin):
    """
    Модель товара.
    Связана с подкатегорией товаров.
    Использует slug
    """

    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    image = models.ImageField(
        upload_to="products/", validators=[validate_image], default="products/images/default.png"
    )
    image_small = ImageSpecField(
        source="image",
        processors=[ResizeToFill(200, 200)],
        format="JPEG",
        options={"quality": 85},
    )

    image_medium = ImageSpecField(
        source="image",
        processors=[ResizeToFill(500, 500)],
        format="JPEG",
        options={"quality": 90},
    )

    image_large = ImageSpecField(
        source="image",
        processors=[ResizeToFill(1000, 1000)],
        format="JPEG",
        options={"quality": 95},
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def category(self):
        return self.subcategory.category

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["name"]
