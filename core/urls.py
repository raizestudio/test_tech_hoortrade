""" URL configuration for the core application."""
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from django.contrib import admin

router = DefaultRouter()

urlpatterns = router.urls
urlpatterns += [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("accounts/", include("accounts.urls")),
]
