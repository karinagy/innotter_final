from rest_framework.permissions import BasePermission

from core.enums.user_enums import Roles


class IsUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return Roles.USER.value in user.role


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return Roles.MODERATOR.value in user.role


class IsAdminOrModerator(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            return Roles.MODERATOR.value in user.role or Roles.ADMIN.value in user.role
        except Exception as e:
            return False
