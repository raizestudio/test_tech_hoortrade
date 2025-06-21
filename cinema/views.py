from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from cinema.models import AuthorReview, Genre, Movie, MovieReview
from cinema.serializers import (
    AuthorReviewSerializer,
    GenreSerializer,
    MovieReviewSerializer,
    MovieSerializer,
)
from core.pagination import DefaultPagination


class GenreViewSet(ModelViewSet):
    """A viewset for viewing and editing genre instances."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class AuthorReviewViewSet(ModelViewSet):
    """A viewset for viewing and editing author review instances."""

    queryset = AuthorReview.objects.all()
    serializer_class = AuthorReviewSerializer


class MovieReviewViewSet(ModelViewSet):
    """A viewset for viewing and editing movie review instances."""

    queryset = MovieReview.objects.all()
    serializer_class = MovieReviewSerializer


class MovieViewSet(ModelViewSet):
    """A viewset for viewing and editing movie instances."""

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filterset_fields = ["title", "status"]
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = DefaultPagination
