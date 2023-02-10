from django.db import models


class UnBlockedUsersManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(is_blocked=True)
