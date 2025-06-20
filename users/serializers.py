from rest_framework import serializers

from users.models import AdminUser, Author, BaseUser, Spectator


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ("id", "username", "email", "is_active", "is_staff", "is_superuser")


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUser
        fields = ("id", "username", "email", "is_active", "is_staff", "is_superuser")


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ("id", "username", "email", "first_name", "last_name", "movies")


class SpectatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spectator
        fields = ("id", "username", "email", "first_name", "last_name", "favorite_movies")
