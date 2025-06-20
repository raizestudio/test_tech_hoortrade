from rest_framework.routers import DefaultRouter

from users.views import (
    AdminUserViewSet,
    AuthorViewSet,
    BaseUserViewSet,
    SpectatorViewSet,
)

router = DefaultRouter()
router.register(r"users", BaseUserViewSet, basename="users")
router.register(r"admin", AdminUserViewSet, basename="admin")
router.register(r"authors", AuthorViewSet, basename="authors")
router.register(r"spectators", SpectatorViewSet, basename="spectators")

urlpatterns = router.urls
