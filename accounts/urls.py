from django.urls import path

from accounts.views import (
    CreateUserView,
    CustomTokenBlacklistView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    CustomTokenVerifyView,
    ManageUserView,
)


app_name = "accounts"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="user-create"),
    path("me/", ManageUserView.as_view(), name="user-manage"),
    path(
        "token/",
        CustomTokenObtainPairView.as_view(),
        name="token-obtain-pair",
    ),
    path(
        "token/refresh/",
        CustomTokenRefreshView.as_view(),
        name="token-refresh",
    ),
    path(
        "token/verify/",
        CustomTokenVerifyView.as_view(),
        name="token-verify",
    ),
    path(
        "token/logout/",
        CustomTokenBlacklistView.as_view(),
        name="token-blacklist",
    ),
]
