from django.db import models


class Roles(models.TextChoices):
    USER = 'user', 'user'
    MODERATOR = 'moderator', 'moderator'
    ADMIN = 'admin', 'admin'


class Gender(models.TextChoices):
    MALE = 'MALE', 'MALE'
    FEMALE = 'FEMALE', 'FEMALE'
