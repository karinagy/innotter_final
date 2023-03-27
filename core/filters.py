from django_filters import rest_framework as filters

from page.models import Page
from user.models import User


class UserFilter(filters.FilterSet):
    username = filters.CharFilter(field_name='username', lookup_expr='icontains')

    class Meta:
        model = User
        fields = ['username']


class PageFilter(filters.FilterSet):
    uuid = filters.CharFilter(field_name='uuid', lookup_expr='icontains')
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = Page
        fields = ['uuid', 'title']
