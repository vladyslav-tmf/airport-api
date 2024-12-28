from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "password", "is_staff")
        read_only_fields = ("id", "is_staff")

    def validate_email(self, value: str) -> str:
        """Validate email field."""
        email = value.lower()

        if User.objects.filter(email__iexact=email).exists():
            if self.instance and self.instance.email.lower() == email:
                return value
            raise serializers.ValidationError(
                {"email": "User with this email already exists."}
            )
        return value

    def validate_first_name(self, value: str) -> str:
        """Validate first_name field."""
        if not value.isalpha():
            raise serializers.ValidationError(
                {"first_name": "First name should only contain letters."}
            )
        return value.strip()

    def validate_last_name(self, value: str) -> str:
        """Validate last_name field."""
        if not value.isalpha():
            raise serializers.ValidationError(
                {"last_name": "Last name should only contain letters."}
            )
        return value.strip()

    def create(self, validated_data: dict):
        """Create a new user with encrypted password and return it."""
        return User.objects.create_user(**validated_data)

    def update(self, instance: User, validated_data: dict):
        """Update a user, set the password correctly and return it."""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
