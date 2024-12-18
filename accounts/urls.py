from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.views import CreateUserView, ManageUserView


app_name = "accounts"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="user-create"),
    path("token/", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("me/", ManageUserView.as_view(), name="user-manage"),
]
