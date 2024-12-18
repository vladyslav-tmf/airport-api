from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    """
    Custom form for user registration that uses email as the unique identifier.

    Extends the build-in UserCreationForm to handle custom user model with
    email authentication instead of username.
    """
    class Meta:
        model = get_user_model()
        fields = ("email", "first_name", "last_name")
