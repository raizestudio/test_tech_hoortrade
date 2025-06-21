from rest_framework import serializers

from cinema.models import AuthorReview, Genre, Movie, MovieReview
from users.serializers import AuthorSerializer


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name"]
        read_only_fields = ["id"]


class MovieReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieReview
        fields = [
            "id",
            "rating",
            "comment",
            "movie",
            "created_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at"]


class AuthorReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorReview
        fields = [
            "id",
            "rating",
            "comment",
            "author",
            "created_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at"]


class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(read_only=True, many=True)
    authors = AuthorSerializer(read_only=True, many=True)

    class Meta:
        model = Movie
        fields = [
            "id",
            "title",
            "description",
            "release_date",
            "rating",
            "status",
            "created_at",
            "updated_at",
            "genres",
            "authors",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
