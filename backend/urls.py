"""
URL configuration for PetLink backend.
"""

from __future__ import annotations

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
	openapi.Info(
		title="PetLink API",
		default_version="v1",
		description="Public API for PetLink features.",
	),
	public=True,
	permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
	path("admin/", admin.site.urls),
	path("accounts/", include("django.contrib.auth.urls")),
	path("", include("portal.urls")),
	path("api/", include("portal.api_urls")),
	path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
	path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
	path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
	path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


