from rest_framework import permissions

class IsAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin

class IsModeratorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_moderator
        
class IsOwnerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                    or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (obj.author == request.user or request.user.is_admin
                or  request.user.is_moderator)

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

                
class ReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS



    