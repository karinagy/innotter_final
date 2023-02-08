from rest_framework import serializers

from page.api.v1.serializers.tag_serializers import TagSerializer
from user.api.v1.serializers.user_serializers import UserSerializer
from page.models import Page


class BlockUserPageSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if not ret['is_blocked']:
            return ret


class PageSerializer(BlockUserPageSerializer):
    tags = TagSerializer(read_only=True, many=True)
    owner = UserSerializer(read_only=True)
    followers = UserSerializer(read_only=True, many=True)
    follow_requests = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Page
        fields = ['id', 'name', 'uuid', 'tags', 'description', 'owner', 'followers', 'is_private', 'follow_requests',
                  'image', 'is_blocked', 'unblock_date']
        read_only_fields = ['followers', 'is_blocked', 'unblock_date']


class PageOwnerSerializer(BlockUserPageSerializer):
    class Meta:
        model = Page
        fields = '__all__'
        read_only_fields = ['is_blocked', 'unblock_date']


class CreatePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['name', 'uuid', 'owner', 'image', 'tags', 'description', 'is_private']


class UpdatePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['name', 'uuid', 'owner', 'image', 'tags', 'description', 'is_private']


class AcceptSubscriptionRequestsSerializer(serializers.ModelSerializer):
    """
    Class serializer to accept subscription request
    """

    class Meta:
        model = Page
        fields = ['follow_requests', 'followers']

    def update(self, page, validated_data):
        users = validated_data.pop('follow_requests')
        for user in users:
            page.follow_requests.remove(user)
            page.followers.add(user)

        page.save()
        return page


class DenySubscriptionRequestsSerializer(serializers.ModelSerializer):
    """
    Class serializer to deny subscription request
    """

    class Meta:
        model = Page
        fields = ['follow_requests']

    def update(self, page, validated_data):
        users = validated_data.pop('follow_requests')
        for user in users:
            page.follow_requests.remove(user)

        page.save()
        return page
