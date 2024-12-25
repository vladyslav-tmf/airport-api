from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated

from accounts.serializers import UserSerializer


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
            )
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
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authenticated.",
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Data validation error.",
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
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authenticated.",
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Data validation error.",
            ),
        },
        tags=("Users",),
    ),
)
class ManageUserView(generics.RetrieveUpdateAPIView):
    """Endpoint for retrieving and updating authenticated user's profile information."""
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        """Get currently authenticated user instance."""
        return self.request.user
