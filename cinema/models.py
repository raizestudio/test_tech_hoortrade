from enum import Enum

from django.db import models
from polymorphic.models import PolymorphicModel

from core.models import DataSource


class MovieStatus(Enum):
    DRAFT = "draft"
    IN_REVIEW = "in_review"
    PUBLISHED = "published"
    ARCHIVED = "archived"

    @classmethod
    def choices(cls):
        return [(tag.name, tag.value) for tag in cls]


class MovieRating(Enum):
    ONE_STAR = 1
    TWO_STARS = 2
    THREE_STARS = 3
    FOUR_STARS = 4
    FIVE_STARS = 5

    @classmethod
    def choices(cls):
        return [(tag.value, tag.value) for tag in cls]


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Review(PolymorphicModel):
    rating = models.IntegerField(choices=MovieRating.choices(), default=MovieRating.THREE_STARS.value)
    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class MovieReview(Review):
    movie = models.ForeignKey("Movie", on_delete=models.CASCADE, related_name="reviews")
    created_by = models.ForeignKey("users.Spectator", on_delete=models.CASCADE, related_name="movies_reviews")

    class Meta:
        unique_together = ("movie", "created_by")

    def __str__(self):
        return f"Review for {self.movie.title}"


class AuthorReview(Review):
    author = models.ForeignKey("users.Author", on_delete=models.CASCADE, related_name="reviews")
    created_by = models.ForeignKey(
        "users.Spectator", on_delete=models.CASCADE, related_name="authors_reviews"
    )

    class Meta:
        unique_together = ("author", "created_by")

    def __str__(self):
        return f"Review for {self.author.username}"


class Movie(models.Model):
    title = models.CharField(max_length=100)
    original_title = models.CharField(max_length=100, null=True, blank=True)
    original_language = models.CharField(max_length=10, null=True, blank=True)
    description = models.TextField()
    release_date = models.DateField()
    status = models.CharField(max_length=20, choices=MovieStatus.choices(), default=MovieStatus.DRAFT.name)
    adult_content = models.BooleanField(default=False)
    poster = models.ImageField(upload_to="posters/", null=True, blank=True)
    source = models.CharField(max_length=50, choices=DataSource.choices(), default=DataSource.API.name)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    genres = models.ManyToManyField(Genre, related_name="movies")
    authors = models.ManyToManyField("users.Author", related_name="movies")

    class Meta:
        unique_together = ("title", "original_title", "release_date")

    def __str__(self):
        return self.title

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if not reviews:
            return None
        total_rating = sum(review.rating for review in reviews)
        return total_rating / len(reviews)
