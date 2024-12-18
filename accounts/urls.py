from django.urls import path

from accounts.views import CreateUserView, ManageUserView


app_name = "accounts"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="user-create"),
    path("me/", ManageUserView.as_view(), name="user-manage"),
]
