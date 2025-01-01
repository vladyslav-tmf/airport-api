from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class UserManager(BaseUserManager):
    """Manager for custom User model with email-based authentication."""

    use_in_migrations = True

    def _create_user(self, email: str, password: str, **extra_fields) -> "User":
        """Create and save a User with the given email and password."""
        if not email:
            raise ValidationError({"email": "The given email must be set."})

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str, **extra_fields) -> "User":
        """Create and save a regular User."""
        if not password:
            raise ValidationError({"password": "Password is required."})

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields) -> "User":
        """Create and save a SuperUser."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff"):
            raise ValidationError({"is_staff": "Superuser must have is_staff=True."})
        if not extra_fields.get("is_superuser"):
            raise ValidationError(
                {"is_superuser": "Superuser must have is_superuser=True."}
            )

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom user model using email for authentication instead of username."""

    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    class Meta:
        ordering = ("last_name", "first_name")

    def clean(self) -> None:
        """Validate required fields."""
        if not self.first_name or not self.last_name:
            raise ValidationError(
                {
                    "first_name": "First name is required.",
                    "last_name": "Last name is required.",
                }
            )

    def save(self, *args, **kwargs) -> None:
        """Call full_clean() before saving the user."""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.get_full_name()
