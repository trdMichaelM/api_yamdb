from rest_framework import permissions


class AdminReadOnlyPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        safe_method = request.method in permissions.SAFE_METHODS
        return bool(safe_method and request.user
                    and request.user.is_authenticated
                    and request.user.is_admin)


class ReadOnlyOrAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        safe_method = request.method in permissions.SAFE_METHODS
        return bool(safe_method or (request.user
                    and request.user.is_authenticated
                    and request.user.is_admin))


class AdminWriteOnlyPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated
                    and request.user.is_admin)


class AdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        user_is_admin = (request.user and request.user.is_authenticated
                         and request.user.role == 'admin')
        user_has_right = (request.user and request.user.is_authenticated
                          and request.user.role == 'moderator')
        return obj.author == request.user or user_is_admin or user_has_right
