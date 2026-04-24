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

from users.models import CustomUser
from users.serializers import LoginSerializer, RegisterSerializer, UserProfileSerializer
from users.tokens import account_activation_token

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
        token = account_activation_token.make_token(user)
        verify_url = self.request.build_absolute_uri(reverse("users:verify-email") + f"?uid={uid}&token={token}")
        send_mail(
            subject="Подтверждение email",
            message=f"Перейдите по ссылке для подтверждения email: {verify_url}",
            from_email=None,
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
            user = CustomUser.objects.get(pk=user_id)
        except Exception:
            return Response({"detail": "Неверная ссылка"}, status=status.HTTP_400_BAD_REQUEST)

        if account_activation_token.check_token(user, token):
            user.is_active = True
            user.is_verified = True
            user.save(update_fields=["is_active", "is_verified"])
            Token.objects.get_or_create(user=user)
            return Response({"detail": "Email подтвержден"}, status=status.HTTP_200_OK)

        return Response({"detail": "Ссылка недействительна или устарела"}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(generics.GenericAPIView):
    """Авторизация пользователя"""

    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

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
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Возвращает объект пользователя"""
        return self.request.user
