"""
URL configuration for schub project.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls.conf import include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("restapi/", include("rest_framework.urls")),
    path("api/", include("core.urls")),
    path("api/", include("school.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
