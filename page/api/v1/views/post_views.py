from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from core.mixins.serializers import DynamicActionSerializerMixin
from page.api.v1.serializers.post_serializers import PostSerializer, CreatePostSerializer, UpdatePostSerializer
from page.models import Post
from page.services import PostService


class PostViewSet(DynamicActionSerializerMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    serializer_action_classes = {
        'create': CreatePostSerializer,
        'update': UpdatePostSerializer,
    }

    def create(self, request, *args, **kwargs):
        data = {**request.data, 'owner': self.request.user.id}
        serializer = self.get_serializer_class()
        serializer = serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        send_mail.delay(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        data = {**request.data, 'owner': self.request.user.id}
        serializer = self.get_serializer_class()
        serializer = serializer(instance=self.get_object(), data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], url_path=r'\w*like', permission_classes=[IsAuthenticated], detail=True)
    def like(self, request, *args, **kwargs):
        msg = PostService.like_unlike_switch(self.get_object(), request)
        return Response(data=msg, status=status.HTTP_201_CREATED)


class FeedViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Post.objects.filter(page__owner=self.request.user.id or Post(page__followers=self.request.user.id),
                                   page__owner__is_blocked=False,
                                   page__is_blocked=False).order_by('-created_at')
