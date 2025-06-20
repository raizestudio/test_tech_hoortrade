from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from polymorphic.managers import PolymorphicManager
from polymorphic.models import PolymorphicModel

from core.models import DataSource


class CustomUserManager(PolymorphicManager, BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        if not email:
            raise ValueError("Email is required")
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class BaseUser(PolymorphicModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    date_of_birth = models.DateField(default="1995-07-16")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.email} ({self.__class__.__name__})"

    def save(self, *args, **kwargs):
        # A user must be a subclass of BaseUser
        if self.__class__ == BaseUser:
            raise TypeError("You cannot create an instance of BaseUser directly. Use a subclass instead.")
        super().save(*args, **kwargs)

    @property
    def is_admin_user(self):
        return isinstance(self, AdminUser)

    @property
    def is_author_user(self):
        return isinstance(self, Author)

    @property
    def is_spectator_user(self):
        return isinstance(self, Spectator)


class AuthorManager(CustomUserManager):
    def get_authors_with_atleast_one_movie(self):
        return self.filter(movies__isnull=False).distinct()


class Author(BaseUser):
    bio = models.TextField(blank=True)
    source = models.CharField(max_length=50, choices=DataSource.choices(), default=DataSource.API.name)

    objects = AuthorManager()


class Spectator(BaseUser):
    preferred_language = models.CharField(max_length=30, default="en")

    favorite_movies = models.ManyToManyField(
        "cinema.Movie",
        blank=True,
        related_name="favorite_spectators",
        through="cinema.FavoriteMovie",
    )


class AdminUser(BaseUser):
    access_level = models.IntegerField(default=1)
