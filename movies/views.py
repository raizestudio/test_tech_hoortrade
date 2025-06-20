from rest_framework.viewsets import ModelViewSet

from movies.models import Genre, Movie, MovieReview, AuthorReview
from movies.serializers import GenreSerializer, MovieSerializer, MovieReviewSerializer, AuthorReviewSerializer


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
    filterset_fields = ['title', "status"]
