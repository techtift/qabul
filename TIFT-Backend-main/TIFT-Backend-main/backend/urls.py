from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from django.views.static import serve

schema_view = get_schema_view(
    openapi.Info(
        title="TIFT API",
        default_version='v1',
        description="API documentation for the TIFT Application",
    ),
    url='https://qabul.tift.uz/',
    # url='http://localhost:8000/',
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[],
)

admin.site.site_header = "TIFT Admin"
admin.site.site_title = "TIFT Admin Portal"
admin.site.index_title = "Welcome to TIFT Admin Portal"

v1_urls = [
    path(
        "api/v1/",
        include(
            [
                path("auth/user/", include("user.urls")),
                path("university/", include("university.urls")),
            ]
        ),
    ),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += v1_urls


urlpatterns += [
    re_path(r'static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
