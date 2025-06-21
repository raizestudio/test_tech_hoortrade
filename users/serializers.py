from rest_framework import serializers

from users.models import AdminUser, Author, BaseUser, Spectator


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ("id", "username", "email", "is_active", "is_staff", "is_superuser")


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        # This will be subclassed, so we don't bind a model here
        model = None
        fields = ("id", "username", "email", "first_name", "last_name", "date_of_birth", "is_active")


class AdminUserSerializer(UserProfileSerializer):
    class Meta(UserProfileSerializer.Meta):
        model = AdminUser
        fields = UserProfileSerializer.Meta.fields + ("is_staff", "is_superuser")


class AuthorSerializer(UserProfileSerializer):
    class Meta(UserProfileSerializer.Meta):
        model = Author
        fields = UserProfileSerializer.Meta.fields + ("movies",)


class SpectatorSerializer(UserProfileSerializer):

    class Meta(UserProfileSerializer.Meta):
        model = Spectator
        fields = UserProfileSerializer.Meta.fields + ("favorite_movies",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from cinema.serializers import MovieSerializer

        self.fields["favorite_movies"] = MovieSerializer(many=True, read_only=True)
