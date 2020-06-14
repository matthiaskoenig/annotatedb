"""adb_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url

from .adb.urls import router

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# elasticsearch endpoints
from .search_indexes import urls as search_index_urls

# swagger REST API
# from rest_framework_swagger.views import get_swagger_view
# schema_view = get_swagger_view(title="ADB API")

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="ADB API",
      default_version='v1',
      description="AnnotateDB API",

      contact=openapi.Contact(email="konigmatt@googlemail.com"),
      license=openapi.License(name="LGPLv3"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    url(r'^api/token/$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'^api/token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
    path(r"api/v1/", include(router.urls)),
    # url(r"api/", schema_view, name="api"),
    url(r'^api(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^api/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    url(r'^search/', include(search_index_urls)),
]
