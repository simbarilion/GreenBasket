from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from .models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации пользователя"""

    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ("email", "username", "password", "password2", "phone_number", "city")

    def validate(self, attrs):
        """Валидация повторного ввода пароля"""
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Пароли не совпадают."})
        return attrs

    def create(self, validated_data):
        """Создает и сохраняет в БД объект пользователя"""
        validated_data.pop("password2")
        password = validated_data.pop("password")
        user = CustomUser(**validated_data)
        user.is_active = False
        user.is_verified = False
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """Сериализатор для авторизации пользователя"""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """Валидация логина и пароля пользователя при входе"""
        email = attrs.get("email")
        password = attrs.get("password")
        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError("Неверный email или пароль")
        if not user.is_verified:
            raise serializers.ValidationError("Email не подтвержден")
        attrs["user"] = user
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор профиля пользователя"""

    class Meta:
        model = CustomUser
        fields = ("id", "email", "username", "phone_number", "city", "is_verified")
        read_only_fields = ("id", "email", "is_verified")
