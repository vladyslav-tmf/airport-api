from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from accounts.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """Endpoint for user registration that creates a new user in the system."""
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Endpoint for retrieving and updating authenticated user's profile information."""
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        """Get currently authenticated user instance."""
        return self.request.user
