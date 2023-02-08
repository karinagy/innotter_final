from django.db import models

from user.models import User


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Page(models.Model):
    name = models.CharField(max_length=80)
    uuid = models.CharField(max_length=32, unique=True)
    tags = models.ManyToManyField(
        Tag,
        related_name='tag_pages'
    )
    description = models.TextField()
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owner_page'
    )
    followers = models.ManyToManyField(
        User,
        related_name='follower_pages',
        blank=True
    )
    is_private = models.BooleanField(default=False)
    follow_requests = models.ManyToManyField(
        User,
        related_name='follow_requests_pages',
        blank=True
    )
    image = models.URLField(null=True, blank=True)
    is_blocked = models.BooleanField(default=False)
    unblock_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.id} {self.name}'


class Post(models.Model):
    page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        related_name='page_posts'
    )
    content = models.CharField(max_length=180)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owner_post'
    )
    liked_by = models.ManyToManyField(
        User,
        related_name='liked_by_posts',
        blank=True
    )
    reply_to = models.ForeignKey(
        'Post',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reply_to_post'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id} {self.content}'
