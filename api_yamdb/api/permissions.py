from rest_framework import permissions


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
                         )
        user_has_right = (
                request.user and request.user.is_authenticated )
        return obj.author == request.user or  user_is_admin or user_has_right
