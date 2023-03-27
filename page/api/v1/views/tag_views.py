from apt_pkg import Tag
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from page.api.v1.serializers.tag_serializers import TagSerializer


class TagViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticated,)
