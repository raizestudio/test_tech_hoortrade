import requests
from django.conf import settings
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from cinema.models import AuthorReview, Genre, Movie, MovieReview, MovieStatus
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

    queryset = MovieReview.objects.select_related(
        "movie",
        "created_by",
        "created_by__polymorphic_ctype",
        "created_by__baseuser_ptr",
        "review_ptr",
        "review_ptr__polymorphic_ctype",
    ).prefetch_related("movie__genres", "movie__authors", "created_by__favorite_movies")
    serializer_class = MovieReviewSerializer


class MovieViewSet(ModelViewSet):
    """A viewset for viewing and editing movie instances."""

    queryset = Movie.objects.prefetch_related("genres", "authors").prefetch_related("reviews").all()
    serializer_class = MovieSerializer
    filterset_fields = ["title", "status", "source"]
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = DefaultPagination

    def get_serializer_class(self):
        if self.action == "review":
            return MovieReviewSerializer
        return super().get_serializer_class()

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
        """Search for movies using the TMDB API."""
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

    @action(detail=False, methods=["get"], url_path="favorite-movies")
    def favorite_movies(self, request):
        """Get the favorite movies of the authenticated spectator user."""
        user = request.user
        # if not user.is_authenticated:
        # return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        if not getattr(user, "is_spectator_user", False):
            return Response(
                {"detail": "Only spectators can access this endpoint."}, status=status.HTTP_403_FORBIDDEN
            )

        favorite_movies_qs = user.favorite_movies.all()
        serializer = self.get_serializer(favorite_movies_qs, many=True, context={"request": request})
        return Response(serializer.data)

    @action(detail=True, methods=["get", "post"], url_path="review")
    def review(self, request, *args, **kwargs):
        """Allow authenticated specator to review a movie."""

        user = request.user
        # if not user.is_authenticated:
        # return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        if not getattr(user, "is_spectator_user", False):
            return Response(
                {"detail": "Only spectators can review movies."}, status=status.HTTP_403_FORBIDDEN
            )

        movie = self.get_object()

        if request.method == "GET":
            reviews = movie.reviews.all()
            serializer = MovieReviewSerializer(reviews, many=True, context={"request": request})
            return Response(serializer.data)

        elif request.method == "POST":
            data = request.data.copy()
            data["movie"] = movie.id
            data["spectator"] = user.id
            serializer = MovieReviewSerializer(data=data, context={"request": request})

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"], url_path="archive")
    def archive(self, request, *args, **kwargs):
        """Archive a movie."""
        user = request.user
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        if not getattr(user, "is_admin_user", False):
            return Response(
                {"detail": "Only admin users can archive movies."}, status=status.HTTP_403_FORBIDDEN
            )

        movie = self.get_object()
        if movie.status == MovieStatus.ARCHIVED:
            return Response({"detail": "Movie is already archived."}, status=status.HTTP_400_BAD_REQUEST)

        movie.status = MovieStatus.ARCHIVED.name
        movie.save()
        return Response({"detail": "Movie archived successfully."}, status=status.HTTP_200_OK)
