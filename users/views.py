from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from cinema.serializers import AuthorReviewSerializer, MovieSerializer
from core.pagination import DefaultPagination
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
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticatedOrReadOnly]


class AdminUserViewSet(ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """

    queryset = AdminUser.objects.all()
    serializer_class = AdminUserSerializer
    filterset_fields = ["username", "email"]
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticatedOrReadOnly]


class AuthorViewSet(ModelViewSet):
    """
    A viewset for viewing and editing author instances.
    """

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filterset_fields = ["username", "email", "source"]
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = DefaultPagination

    def get_serializer_class(self):
        if self.action == "review":
            return AuthorReviewSerializer
        return super().get_serializer_class()

    def destroy(self, request, *args, **kwargs):
        author = self.get_object()
        if author.movies.exists():
            return Response(
                {"detail": "You cannot delete an author who has movies."}, status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=["get", "post"], url_path="review")
    def review(self, request, *args, **kwargs):
        """Allow authenticated spectators to review an author"""

        user = request.user
        if not user.is_authenticated or not isinstance(user, Spectator):
            return Response(
                {"detail": "You must be a spectator to review an author."}, status=status.HTTP_403_FORBIDDEN
            )
        author = self.get_object()

        if request.method == "GET":
            reviews = author.reviews.all()
            serializer = AuthorReviewSerializer(reviews, many=True, context={"request": request})
            return Response(serializer.data)

        elif request.method == "POST":
            data = request.data.copy()
            data["author"] = author.id
            data["spectator"] = user.id
            serializer = AuthorReviewSerializer(data=data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SpectatorViewSet(ModelViewSet):
    """
    A viewset for viewing and editing spectator instances.
    """

    queryset = Spectator.objects.all()
    serializer_class = SpectatorSerializer
    filterset_fields = ["username", "email"]
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=["get"], url_path="favorite-movies")
    def favorite_movies(self, request, pk=None):
        spectator = self.get_object()
        movies = spectator.favorite_movies.all()
        serializer = MovieSerializer(movies, many=True, context={"request": request})
        return Response(serializer.data)
