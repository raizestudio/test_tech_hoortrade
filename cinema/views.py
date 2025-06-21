import requests
from django.conf import settings
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
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

    @extend_schema(
        parameters=[
            OpenApiParameter(name="query", type=str, description="Search query for TMDB API", required=True),
            OpenApiParameter(
                name="page",
                type=int,
                description="Page number for TMDB API results",
                required=False,
                default=1,
            ),
            OpenApiParameter(
                name="include_adult",
                type=bool,
                description="Whether to include adult content in the search results",
                required=False,
                default=False,
            ),
        ],
        # responses={200: MovieSerializer(many=True), 400: "Bad Request", 502: "Bad Gateway"},
    )
    @action(detail=False, methods=["get"], url_path="tmdb-search")
    def tmdb_search(self, request):
        query = request.query_params.get("query")
        page = request.query_params.get("page", 1)
        include_adult = request.query_params.get("include_adult", "false").lower() == "true"

        if not query:
            return Response({"detail": "Missing 'query' parameter."}, status=status.HTTP_400_BAD_REQUEST)

        url = "https://api.themoviedb.org/3/search/movie"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {settings.TMDB_API_KEY}",
        }
        params = {"query": query, "include_adult": include_adult, "language": "en-US", "page": page}

        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            return Response(
                {"detail": "TMDB API error", "status_code": response.status_code},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        return Response(response.json(), status=status.HTTP_200_OK)
