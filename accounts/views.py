from django.contrib.auth import get_user_model
from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
    TokenVerifySerializer,
)
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from accounts.serializers import UserSerializer
from airport.api_schema import SERVER_ERROR_500_RESPONSE, UNAUTHORIZED_401_RESPONSE, VALIDATION_400_RESPONSE

User = get_user_model()


@extend_schema_view(
    post=extend_schema(
        description="Register a new user in the system.",
        request=UserSerializer,
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response=UserSerializer,
                description="User successfully created.",
            ),
            **VALIDATION_400_RESPONSE,
            **SERVER_ERROR_500_RESPONSE,
        },
        tags=("Users",),
    )
)
class CreateUserView(generics.CreateAPIView):
    """Endpoint for user registration that creates a new user in the system."""

    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


@extend_schema_view(
    get=extend_schema(
        description="Retrieve currently authenticated user's profile information.",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=UserSerializer,
                description="User profile successfully retrieved.",
            ),
            **UNAUTHORIZED_401_RESPONSE,
            **SERVER_ERROR_500_RESPONSE,
        },
        tags=("Users",),
    ),
    put=extend_schema(
        description="Fully update currently authenticated user's profile information.",
        request=UserSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=UserSerializer,
                description="User profile successfully updated.",
            ),
            **VALIDATION_400_RESPONSE,
            **UNAUTHORIZED_401_RESPONSE,
            **SERVER_ERROR_500_RESPONSE,
        },
        tags=("Users",),
    ),
    patch=extend_schema(
        description="Partial update of user's profile information.",
        request=UserSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=UserSerializer,
                description="User profile successfully updated.",
            ),
            **VALIDATION_400_RESPONSE,
            **UNAUTHORIZED_401_RESPONSE,
            **SERVER_ERROR_500_RESPONSE,
        },
        tags=("Users",),
    ),
)
class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage authenticated user's profile."""

    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self) -> User:
        """Get current user."""
        return self.request.user


@extend_schema_view(
    post=extend_schema(
        description="Obtain JWT token pair.",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=TokenObtainPairSerializer,
                description="Successfully obtained JWT token pair.",
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="Invalid credentials provided.",
            ),
            **SERVER_ERROR_500_RESPONSE,
        },
        tags=("Authentication",),
    )
)
class CustomTokenObtainPairView(TokenObtainPairView):
    """JWT token pair endpoint."""


@extend_schema_view(
    post=extend_schema(
        description="Obtain new access token using refresh token.",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=TokenRefreshSerializer,
                description="Successfully refresh access token using refresh token.",
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="Refresh token is invalid or expired.",
            ),
            **SERVER_ERROR_500_RESPONSE,
        },
        tags=("Authentication",),
    )
)
class CustomTokenRefreshView(TokenRefreshView):
    """JWT token refresh endpoint."""


@extend_schema_view(
    post=extend_schema(
        description="Verify JWT token validity.",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=TokenVerifySerializer,
                description="JWT token is valid.",
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="JWT token is invalid or expired.",
            ),
            **SERVER_ERROR_500_RESPONSE,
        },
        tags=("Authentication",),
    )
)
class CustomTokenVerifyView(TokenVerifyView):
    """JWT token verification endpoint."""


@extend_schema_view(
    post=extend_schema(
        description="Blacklist JWT token (logout).",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="JWT token successfully blacklisted.",
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="JWT token is invalid or expired.",
            ),
            **SERVER_ERROR_500_RESPONSE,
        },
        tags=("Authentication",),
    )
)
class CustomTokenBlacklistView(TokenBlacklistView):
    """JWT token blacklist (logout) endpoint."""
