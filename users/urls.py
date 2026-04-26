from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from users.views import (
    CustomTokenView,
    LogoutView,
    PasswordResetConfirmView,
    PasswordResetRequestView,
    RegisterView,
    UserProfileView,
    VerifyEmailView,
)

app_name = "users"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("activate/", VerifyEmailView.as_view(), name="activate"),
    path("login/", CustomTokenView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password_reset/", PasswordResetRequestView.as_view(), name="password_reset"),
    path("password_reset_confirm/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
]
