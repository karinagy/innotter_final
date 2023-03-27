from rest_framework.permissions import BasePermission, SAFE_METHODS

from core.enums.user_enums import Roles


class IsUser(BasePermission):
    def has_permission(self, request, view):
        return Roles.USER in request.user.role


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return Roles.MODERATOR in request.user.role


class IsAdminOrModerator(BasePermission):
    def has_permission(self, request, view):
        return Roles.MODERATOR in request.user.role or Roles.ADMIN in request.user.role


class PageAccessPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
                request.method in SAFE_METHODS or
                obj.owner == request.user
                or request.user.is_staff
        )


class IsPageOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
