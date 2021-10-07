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
