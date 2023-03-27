from rest_framework import routers

from page.api.v1.views.page_views import PageViewSet
from page.api.v1.views.post_views import PostViewSet, FeedViewSet
from page.api.v1.views.tag_views import TagViewSet
from user.api.v1.views.user_views import UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'tags', TagViewSet)
router.register(r'pages', PageViewSet)
router.register(r'posts', PostViewSet)
router.register(r'register', UserViewSet)
router.register(r'feed', FeedViewSet, basename='Feed')

urlpatterns = router.urls