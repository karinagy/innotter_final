from rest_framework import serializers

from page.api.v1.serializers.page_serializers import PageSerializer
from page.models import Post, Page

ALLOWED_IMAGE_EXTENSIONS = ('jpg', 'png', 'jpeg', 'gif', 'jpeg')


class PostSerializer(serializers.ModelSerializer):
    page = PageSerializer()

    class Meta:
        model = Post
        fields = (
            'id',
            'page',
            'created_at',
            'updated_at',
            'reply_to',
            'liked_by'
        )


class CreatePostSerializer(serializers.ModelSerializer):
    page = PageSerializer()

    class Meta:
        model = Post
        fields = (
            'id',
            'page',
            'content',
            'owner',
            'reply_to'
        )


class UpdatePostSerializer(serializers.ModelSerializer):
    page = PageSerializer()

    class Meta:
        model = Post
        fields = (
            'id',
            'page',
            'content',
            'owner',
            'reply_to'
        )


class LikedPostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        depth = 1
        fields = (
            'id',
            'page_post'
        )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        posts = ret.pop('page_post')
        for i, post in enumerate(posts):
            if not post['liked_by']:
                posts.pop(i)

        ret['page_post'] = posts
        return ret


class ImageSerializer(serializers.ModelSerializer):
    @staticmethod
    def validate_extension(image):
        extension = image.rsplit('.')[-1]
        if extension.lower() not in ALLOWED_IMAGE_EXTENSIONS:
            raise serializers.ValidationError(
                {'status': f'Invalid uploaded image type: {image}'}
            )
