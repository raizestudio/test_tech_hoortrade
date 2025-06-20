"""URL configuration for the core application."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from core.views import RootView

router = DefaultRouter()

urlpatterns = (
    [
        path("", RootView.as_view(), name="api-root"),
        path('api-auth/', include('rest_framework.urls')),
        path("admin/", admin.site.urls),
        path("users/", include("users.urls")),
        path("accounts/", include("accounts.urls")),
        path("movies/", include("movies.urls")),
    ]
    + router.urls
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
