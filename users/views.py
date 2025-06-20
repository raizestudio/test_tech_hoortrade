from rest_framework.viewsets import ModelViewSet

from users.models import AdminUser, Author, BaseUser, Spectator
from users.serializers import (
    AdminUserSerializer,
    AuthorSerializer,
    BaseUserSerializer,
    SpectatorSerializer,
)
from movies.serializers import MovieSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

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

    def destroy(self, request, *args, **kwargs):
        author = self.get_object()
        if author.movies.exists():
            return Response(
                {"detail": "You cannot delete an author who has movies."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)


class SpectatorViewSet(ModelViewSet):
    """
    A viewset for viewing and editing spectator instances.
    """

    queryset = Spectator.objects.all()
    serializer_class = SpectatorSerializer
    filterset_fields = ["username", "email"]

    @action(detail=True, methods=['get'], url_path='favorite-movies')
    def favorite_movies(self, request, pk=None):
        spectator = self.get_object()
        movies = spectator.favorite_movies.all() 
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
