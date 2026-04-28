from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    """
    Сериализатор регистрации пользователя:
    - проверка совпадения паролей
    - валидация пароля через Django validators
    - создание неактивного пользователя
    """

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)
    username = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ("email", "username", "password", "password2", "phone_number", "city")

    def validate(self, attrs):
        """Валидация повторного ввода пароля"""
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return attrs

    def create(self, validated_data):
        """Создает и сохраняет в БД объект неактивного пользователя"""
        validated_data.pop("password2")
        password = validated_data.pop("password")
        user = CustomUser.objects.create_user(password=password, is_active=False, is_verified=False, **validated_data)
        return user


class CustomTokenSerializer(TokenObtainPairSerializer):
    """JWT-сериализатор для аутентификации по email вместо username"""

    username_field = "email"


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор профиля пользователя"""

    class Meta:
        model = CustomUser
        fields = ("email", "username", "phone_number", "city", "is_verified")
        read_only_fields = ("email", "is_verified")


class PasswordResetRequestSerializer(serializers.Serializer):
    """Сериализатор для сброса пароля"""

    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Сериализатор подтверждения сброса пароля:
    Ожидает:
    - uid пользователя
    - токен
    - новый пароль
    """

    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(
        write_only=True,
        validators=[
            validate_password,
        ],
    )

    def validate(self, attrs):
        return attrs


class EmptySerializer(serializers.Serializer):
    pass
