from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadCreateOnly(BasePermission):
    """
    Custom permission class that allows:
    - Admin users to perform any action.
    - Authenticated users to perform read and create operations.
    - Unauthenticated users to perform only read operations.
    """
    def has_permission(self, request, view):
        """Check if user has permission to perform action."""
        if not request.user.is_authenticated:
            return request.method in SAFE_METHODS
        if request.user.is_staff:
            return True
        return request.method in SAFE_METHODS + ("POST",)

    def has_object_permission(self, request, view, obj):
        """Check if user has permission to perform action on specific object."""
        if request.user.is_staff:
            return True
        return request.method in SAFE_METHODS
