from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import Author, BaseUser, Spectator


class RegisterSerializer(serializers.Serializer):
    USER_TYPE_CHOICES = (("author", "Author"), ("spectator", "Spectator"))

    user_type = serializers.ChoiceField(choices=USER_TYPE_CHOICES, write_only=True)
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    def validate(self, data):
        return data

    def create(self, validated_data):
        user_type = validated_data.pop("user_type")
        password = validated_data.pop("password")

        if user_type == "author":
            user = Author.objects.create_user(**validated_data)
        elif user_type == "spectator":
            validated_data.pop("bio", None)  # just in case
            user = Spectator.objects.create_user(**validated_data)
        else:
            raise serializers.ValidationError("Invalid user type.")

        user.set_password(password)
        user.save()
        return user


class BaseUserTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs["email"]
        password = attrs["password"]

        user = BaseUser.objects.filter(email=email).first()
        if user and user.check_password(password):
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled.")
            refresh = RefreshToken.for_user(user)
            return {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user_type": user.__class__.__name__.lower(),
                "email": user.email,
            }

        raise serializers.ValidationError("Invalid credentials")
