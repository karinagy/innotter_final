from django.db import models
from django.contrib.auth.models import AbstractUser

from core.enums.user_enums import Roles, Gender


class User(AbstractUser):
    first_name = models.CharField(max_length=64)
    second_name = models.CharField(max_length=64)
    gender = models.CharField(
        max_length=6,
        choices=Gender.choices,
        default=Gender.MALE,
        blank=False
    )
    username = models.CharField(max_length=32, unique=True)
    email = models.EmailField(unique=True)
    image_s3_path = models.CharField(max_length=200, null=True, blank=True)
    role = models.CharField(
        max_length=9,
        choices=Roles.choices,
        default=Roles.USER,
        blank=False
    )
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        name = self.username
        if self.role == Roles.USER.value:
            name = f'user {name}'
        elif self.role == Roles.MODERATOR.value:
            name = f'moderator {name}'
        elif self.role == Roles.ADMIN.value:
            name = f'admin {name}'
        return name
