from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Allows:
    - Admins all operations except DELETE.
    - All users read-only access.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return bool(request.user and request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return bool(request.user and request.user.is_staff)


class IsAdminOrAuthenticatedReadOnly(BasePermission):
    """
    Allows:
    - Admins all operations except DELETE.
    - Authenticated users read-only access.
    - Anonymous users no access.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_staff:
            return request.method != "DELETE"

        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsAdminOrAuthenticatedCreateOnly(BasePermission):
    """
    Allows:
    - Admins all operations except DELETE.
    - Authenticated users read and create access.
    - Anonymous users no access.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_staff:
            return request.method != "DELETE"

        return request.method in SAFE_METHODS + ("POST",)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
