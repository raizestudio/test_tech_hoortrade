from rest_framework import serializers

from cinema.models import AuthorReview, Genre, Movie, MovieReview
from users.serializers import SpectatorSerializer


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name"]
        read_only_fields = ["id"]


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

    class Meta:
        model = Movie
        fields = [
            "id",
            "title",
            "original_title",
            "original_language",
            "description",
            "release_date",
            "status",
            "created_at",
            "updated_at",
            "genres",
            "authors",
            "adult_content",
            "poster",
            "source",
            "average_rating",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "average_rating"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from users.serializers import AuthorSerializer

        self.fields["authors"] = AuthorSerializer(many=True, read_only=True)

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        user = self.context.get("request").user
        if not user.is_authenticated or not getattr(user, "is_admin_user", False):
            rep.pop("source", None)

        return rep


class MovieReviewSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    created_by = SpectatorSerializer(read_only=True)

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
