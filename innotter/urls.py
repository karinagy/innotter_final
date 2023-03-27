"""innotter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from rest_framework_swagger.views import get_swagger_view
from rest_framework_simplejwt.views import TokenVerifyView, TokenObtainPairView, TokenRefreshView

schema_view = get_swagger_view(title='API v1')

api_v1_urls = ([
                   path('', include('api.v1.urls')),
                   path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                   path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
                   path('login/verify', TokenVerifyView.as_view(), name='token_verify'),
               ], 'api_v1')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(api_v1_urls)),
    path('api/swagger/', schema_view),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
