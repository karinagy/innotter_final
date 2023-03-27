from django.contrib.auth.models import UserManager
from django.contrib.auth.hashers import make_password

from core.enums.user_enums import Roles


class CustomUserManager(UserManager):
    def create_user(self, email: str, password: str, username: str, role: str = Roles.USER, is_blocked: bool = False):
        if not email:
            raise ValueError('Email is required')
        if not password:
            raise ValueError('Password is required')
        user = self.model(
            email=self.normalize_email(email),
        )
        password = make_password(password)
        user.set_password(password)
        user.username = username
        user.role = role
        user.is_blocked = is_blocked
        user.is_active = True
        if user.role == Roles.MODERATOR:
            user.is_staff = True
            user.is_superuser = False
            user.save()
            return user
        user.is_staff = False
        user.is_superuser = False
        user.save()
        return user

    def create_superuser(self, email: str, password: str, username: str, role: str = Roles.ADMIN,
                         is_blocked: bool = False):
        if not email:
            raise ValueError('Email is required')
        if not password:
            raise ValueError('Password is required')
        user = self.model(
            email=self.normalize_email(email)
        )
        password = make_password(password)
        user.set_password(password)
        user.username = username
        user.role = role
        user.is_blocked = is_blocked
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user
