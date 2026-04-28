import json
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction

from catalog.models import Category, Product, SubCategory
from config import settings
from users.models import CustomUser


class Command(BaseCommand):
    help = "Заполнение базы данных тестовыми данными"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Заполнение базы данных ...")
        Product.objects.all().delete()
        SubCategory.objects.all().delete()
        Category.objects.all().delete()

        self.create_users()
        self.create_catalog()

        self.stdout.write(self.style.SUCCESS("Данные успешно загружены"))

    def create_users(self):
        try:
            if not CustomUser.objects.filter(email="admin@example.com").exists():
                CustomUser.objects.create_superuser(
                    email="admin@example.com",
                    password="admin123",
                    username="admin",
                )
                self.stdout.write(self.style.SUCCESS("Суперпользователь admin@example.com успешно создан"))
            else:
                self.stdout.write(self.style.WARNING("Суперпользователь admin@example.com уже существует"))
        except IntegrityError as e:
            self.stdout.write(self.style.ERROR(f"Ошибка создания суперпользователя: {e}"))

        try:
            for i in range(3):
                email = f"user{i}@example.com"
                if not CustomUser.objects.filter(email=email).exists():
                    CustomUser.objects.create_user(
                        email=email,
                        password="user123",
                        username=f"user{i}",
                    )
            self.stdout.write(self.style.SUCCESS("Тестовые пользователи успешно созданы"))
        except IntegrityError as e:
            self.stdout.write(self.style.ERROR(f"Ошибка создания пользователей: {e}"))

    def create_catalog(self):
        self.stdout.write("Создание каталога...")

        file_path = Path(settings.BASE_DIR) / "catalog" / "fixtures" / "catalog_data.json"

        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)

        for cat_data in data:
            category = Category.objects.create(
                name=cat_data["name"],
                image=cat_data["image"],
            )

            for sub_data in cat_data["subcategories"]:
                subcategory = SubCategory.objects.create(
                    name=sub_data["name"],
                    category=category,
                    image=sub_data["image"],
                )

                for prod_data in sub_data["products"]:
                    Product.objects.create(
                        name=prod_data["name"],
                        subcategory=subcategory,
                        price=prod_data["price"],
                        image="products/images/default.png",
                    )
