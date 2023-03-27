from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from core.filters import UserFilter
from core.managers import AWSManager
from core.permissions import IsAdminOrModerator
from core.serializers import DynamicActionSerializerMixin
from core.services import PageService
from page.api.v1.serializers.post_serializers import ImageSerializer
from user.api.v1.serializers.user_serializers import UserSerializer, CreateUserSerializer
from user.models import User


class UserViewSet(DynamicActionSerializerMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    permissions_mapping = {
        'create': AllowAny,
        'retrieve': IsAdminOrModerator,
        'update': IsAdminOrModerator,
        'destroy': IsAdminUser,
        'list': IsAdminOrModerator,
    }
    serializer_action_classes = {
        'create': CreateUserSerializer,
    }

    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserFilter

    def perform_create(self, serializer):
        if 'image' in self.request.data:
            ImageSerializer.validate_extension(self.request.data['image'])
            image = AWSManager.upload_file(self.request.data['image'], 'user' + str(User.objects.latest('id').id + 1))
            serializer.validated_data['image'] = image

        if 'password' in self.request.data:
            password = make_password(self.request.data['password'])
            serializer.save(password=password)
        else:
            serializer.save()

    def get_permissions(self):
        for actions, permission in self.permissions_mapping.items():
            if self.action in actions:
                self.permission_classes = (permission,)
        return super(self.__class__, self).get_permissions()

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()
        serializer = serializer(instance=self.get_object(), data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        PageService.block_unblock_switch(user_id=int(kwargs['pk']), is_blocked=bool(serializer.data['is_blocked']))
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        serializer = UserSerializer(self.queryset, many=True)
        for user in serializer.data:
            user['image'] = AWSManager.create_presigned_url(key=user['image'])
        return Response(serializer.data)

    def retrieve(self, request, pk):
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = UserSerializer(user)
        data = serializer.data
        image = AWSManager.create_presigned_url(key=data['image'])
        data['image'] = image
        return Response(data)
