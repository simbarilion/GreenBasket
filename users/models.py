from django.contrib.auth.models import AbstractUser
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class City(models.Model):
    """
    Модель города.
    Используется для хранения списка городов и связи с пользователями.
    """

    name = models.CharField(max_length=100, unique=True, verbose_name="Город")

    def __str__(self):
        """Строковое отображение города"""
        return self.name


class CustomUser(AbstractUser):
    """
    Расширенная модель пользователя:
    - аутентификация по email (USERNAME_FIELD)
    - дополнительное поле phone_number
    - связь с моделью City
    - флаг is_verified для подтверждения email
    """

    email = models.EmailField(unique=True, verbose_name="Email")
    phone_number = PhoneNumberField(
        region="RU", blank=True, null=True, verbose_name="Номер телефона", help_text="Необязательное поле"
    )
    city = models.ForeignKey(
        City, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Город", related_name="users"
    )
    is_verified = models.BooleanField(default=False, verbose_name="Email подтвержден")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        """Строковое отображение пользователя"""
        return self.email

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
        ordering = [
            "email",
        ]
