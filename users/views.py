from rest_framework.viewsets import ModelViewSet

from users.models import AdminUser, Author, BaseUser, Spectator
from users.serializers import (
    AdminUserSerializer,
    AuthorSerializer,
    BaseUserSerializer,
    SpectatorSerializer,
)


class BaseUserViewSet(ModelViewSet):
    """
    A viewset for viewing and editing base user instances.
    """

    queryset = BaseUser.objects.all()
    serializer_class = BaseUserSerializer
    filterset_fields = ["username", "email", "is_active", "is_staff", "is_superuser"]


class AdminUserViewSet(ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """

    queryset = AdminUser.objects.all()
    serializer_class = AdminUserSerializer
    filterset_fields = ["username", "email"]


class AuthorViewSet(ModelViewSet):
    """
    A viewset for viewing and editing author instances.
    """

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filterset_fields = ["username", "email"]


class SpectatorViewSet(ModelViewSet):
    """
    A viewset for viewing and editing spectator instances.
    """

    queryset = Spectator.objects.all()
    serializer_class = SpectatorSerializer
    filterset_fields = ["username", "email"]
