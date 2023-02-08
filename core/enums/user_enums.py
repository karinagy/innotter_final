from django.db import models


class Roles(models.TextChoices):
    USER = 'USER', 'USER'
    MODERATOR = 'MODERATOR', 'MODERATOR'
    ADMIN = 'ADMIN', 'ADMIN'


class Gender(models.TextChoices):
    MALE = 'MALE', 'MALE'
    FEMALE = 'FEMALE', 'FEMALE'
