import logging

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from config import settings
from users.serializers import (
    LoginSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    RegisterSerializer,
    UserProfileSerializer,
)
from users.tokens import token_generator

logger = logging.getLogger("green_basket.users")
User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """Регистрация пользователя"""

    serializer_class = RegisterSerializer
    queryset = User.objects.all()
    permission_classes = [
        AllowAny,
    ]

    def perform_create(self, serializer):
        """
        Валидирует и сохраняет данные пользователя без активации аккаунта.
        Отправляет email пользователю для подтверждения регистрации
        """
        user = serializer.save()
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)
        verify_url = self.request.build_absolute_uri(reverse("users:activate") + f"?uid={uid}&token={token}")
        send_mail(
            subject="Подтверждение регистрации",
            message=f"Перейдите по ссылке для для активации: {verify_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )


class VerifyEmailView(generics.GenericAPIView):
    """Активация аккаунта через ссылку на email пользователя"""

    permission_classes = [AllowAny]

    def get(self, request):
        """Проверяет ссылку для активации аккаунта пользователя, активирует аккаунт"""
        uid = request.query_params.get("uid")
        token = request.query_params.get("token")

        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except Exception:
            return Response({"detail": "Неверная ссылка"}, status=status.HTTP_400_BAD_REQUEST)

        if token_generator.check_token(user, token):
            user.is_active = True
            user.is_verified = True
            user.save(update_fields=["is_active", "is_verified"])
            Token.objects.get_or_create(user=user)
            return Response({"detail": "Email подтвержден"}, status=status.HTTP_200_OK)

        return Response({"detail": "Ссылка недействительна или устарела"}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(generics.GenericAPIView):
    """Авторизация пользователя"""

    serializer_class = LoginSerializer
    permission_classes = [
        AllowAny,
    ]

    def post(self, request):
        """Проверяет пользователя по токену"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Профиль пользователя"""

    serializer_class = UserProfileSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_object(self):
        """Возвращает объект пользователя"""
        return self.request.user


class LogoutView(generics.GenericAPIView):
    """Выход пользователя из профиля"""

    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except Exception:
            pass
        return Response({"detail": "Успешный выход из профиля"}, status=status.HTTP_200_OK)


class PasswordResetRequestView(generics.GenericAPIView):
    """Сброс пароля аккаунта пользователя"""

    serializer_class = PasswordResetRequestSerializer
    permission_classes = [
        AllowAny,
    ]

    def post(self, request):
        """Сброс пароля, отправка письма для подтверждения"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = User.objects.filter(email=email).first()
        if not user:
            return Response(
                {"detail": "Если адрес электронной почты существует, будет отправлена ссылка для сброса пароля"},
                status=status.HTTP_200_OK,
            )

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)
        reset_link = f"http://localhost:8000/api/users/password-reset-confirm/?uid={uid}&token={token}"

        send_mail(
            subject="Password reset",
            message=f"Reset link: {reset_link}",
            from_email=None,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return Response(
            {"detail": "Если адрес электронной почты существует, будет отправлена ссылка для сброса пароля"},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(generics.GenericAPIView):
    """Изменение пароля аккаунта пользователя"""

    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [
        AllowAny,
    ]

    def post(self, request):
        """Подтверждение смены пароля, сохранение нового пароля"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uid = serializer.validated_data["uid"]
        token = serializer.validated_data["token"]
        new_password = serializer.validated_data["new_password"]

        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except Exception:
            return Response({"detail": "Ссылка недействительна или устарела"}, status=status.HTTP_400_BAD_REQUEST)

        if not token_generator.check_token(user, token):
            return Response({"detail": "Недействительный токен"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save(update_fields=["password"])
        Token.objects.filter(user=user).delete()

        return Response({"detail": "Пароль успешно изменен"}, status=status.HTTP_200_OK)
