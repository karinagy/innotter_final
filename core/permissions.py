from rest_framework.permissions import BasePermission

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