from django.contrib.auth import get_user_model
from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from accounts.serializers import UserSerializer


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
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Data validation error.",
            ),
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
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authenticated.",
            ),
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
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Data validation error.",
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authenticated.",
            ),
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
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Data validation error.",
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authenticated.",
            ),
        },
        tags=("Users",),
    ),
)
class ManageUserView(generics.RetrieveUpdateAPIView):
    """Endpoint for retrieving and updating authenticated user's profile information."""

    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self) -> User:
        """Get currently authenticated user instance."""
        return self.request.user


@extend_schema_view(
    post=extend_schema(
        description="Obtain JWT token pair.",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=UserSerializer,
                description="Successfully obtained JWT token pair.",
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="Invalid credentials provided.",
            ),
        },
        tags=("Authentication",),
    )
)
class CustomTokenObtainPairView(TokenObtainPairView):
    """Endpoint for obtaining JWT token pair."""


@extend_schema_view(
    post=extend_schema(
        description="Obtain new access token using refresh token.",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=UserSerializer,
                description="Successfully refresh access token using refresh token.",
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="Refresh token is invalid or expired.",
            ),
        },
        tags=("Authentication",),
    )
)
class CustomTokenRefreshView(TokenRefreshView):
    """Endpoint for refreshing access token using refresh token."""


@extend_schema_view(
    post=extend_schema(
        description="Verify JWT token validity.",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="JWT token is valid.",
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="JWT token is invalid or expired.",
            ),
        },
        tags=("Authentication",),
    )
)
class CustomTokenVerifyView(TokenVerifyView):
    """Endpoint for verifying JWT token."""


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
        },
        tags=("Authentication",),
    )
)
class CustomTokenBlacklistView(TokenBlacklistView):
    """Endpoint for blacklisting JWT token (logout)."""
