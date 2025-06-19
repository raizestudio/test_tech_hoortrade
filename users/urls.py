from rest_framework.routers import DefaultRouter

from users.views import (
    BaseUserViewSet,
)

router = DefaultRouter()

router.register(r"", BaseUserViewSet, basename="base-user")

urlpatterns = router.urls
