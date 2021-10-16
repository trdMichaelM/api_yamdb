from rest_framework import permissions
from rest_framework import permissions


class AdminReadOnlyPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        safe_method = request.method in permissions.SAFE_METHODS
        user_is_admin = (request.user and request.user.is_authenticated
                         and request.user.role == 'admin')
        access = safe_method and user_is_admin
        return access or request.user.is_superuser


class AdminWriteOnlyPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        user_is_admin = (request.user and request.user.is_authenticated
                         and request.user.role == 'admin')
        return user_is_admin or request.user.is_superuser

class AdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return(
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        user_is_admin = (request.user and request.user.is_authenticated
                         and request.user.role == 'admin')
        user_has_right = (
                request.user and request.user.is_authenticated and
                request.user.role == 'moderator')
        return obj.author == request.user or  user_is_admin or user_has_right
        
# class AdminModeratorUserReadOnlyPermissions(permissions.BasePermission):
#     def has_permission(self, request, view):
#         safe_method = request.method in permissions.SAFE_METHODS
#         user_has_right = (
#                 request.user and request.user.is_authenticated and
#                 request.user.role in ('admin', 'moderator', 'user',)
#         )
#         access = safe_method and user_has_right
#         return access or request.user.is_superuser
#
#
# class AdminModeratorUserWriteOnlyPermissions(permissions.BasePermission):
#     def has_permission(self, request, view):
#         user_has_right = (
#                 request.user and request.user.is_authenticated and
#                 request.user.role in ('admin', 'moderator', 'user',)
#         )
#         return user_has_right or request.user.is_superuser


# class SuperUserPermissions(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return bool(request.user and request.user.is_superuser)