from django.urls import path

from users.views import (
    LogoutView,
    PasswordResetConfirmView,
    PasswordResetRequestView,
    RegisterView,
    UserLoginView,
    UserProfileView,
    VerifyEmailView,
)

app_name = "users"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("activate/", VerifyEmailView.as_view(), name="activate"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password_reset/", PasswordResetRequestView.as_view(), name="password_reset"),
    path("password_reset_confirm/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
]
