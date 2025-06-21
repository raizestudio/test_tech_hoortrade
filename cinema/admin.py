from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html_join

from cinema.filters import AverageRatingFilter
from cinema.models import AuthorReview, FavoriteMovie, Genre, Movie, MovieReview
from core.models import DataSource


class AuthorInline(admin.TabularInline):
    model = Movie.authors.through
    extra = 1
    verbose_name = "Author"
    verbose_name_plural = "Authors"


class GenreInline(admin.TabularInline):
    model = Movie.genres.through
    extra = 1
    verbose_name = "Genre"
    verbose_name_plural = "Genres"


admin.site.register(Genre)
admin.site.register(MovieReview)
admin.site.register(AuthorReview)
admin.site.register(FavoriteMovie)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Admin interface for managing movies."""

    inlines = [AuthorInline, GenreInline]
    list_display = (
        "title",
        "original_title",
        "original_language",
        "release_date",
        "status",
        "average_rating",
        "source",
        "created_at",
        "updated_at",
    )
    search_fields = ("title", "original_title")
    list_filter = ("status", "release_date", "source", AverageRatingFilter)
    ordering = ("-release_date",)

    fieldsets = (
        (None, {"fields": ("title", "description", "release_date", "status")}),
        ("Additional Information", {"fields": ("source",)}),
        ("Reviews", {"fields": ("reviews_list",)}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )
    readonly_fields = ("created_at", "updated_at", "genres_list", "authors_list", "reviews_list")

    def save_model(self, request, obj, form, change):
        if not change:
            obj.source = DataSource.ADMIN.name
        super().save_model(request, obj, form, change)

    def genres_list(self, obj):
        genres = obj.genres.all()
        if not genres.exists():
            return "-"
        links = format_html_join(
            ", ",
            '<a href="{}">{}</a>',
            (
                (
                    reverse("admin:cinema_genre_change", args=[genre.pk]),
                    genre.name,
                )
                for genre in genres
            ),
        )
        return links

    def authors_list(self, obj):
        authors = obj.author.all()
        if not authors.exists():
            return "-"

        links = format_html_join(
            ", ",
            '<a href="{}">{}</a>',
            (
                (
                    reverse("admin:users_author_change", args=[author.pk]),
                    author.username,
                )
                for author in authors
            ),
        )
        return links

    def reviews_list(self, obj):
        reviews = obj.reviews.all()
        if not reviews.exists():
            return "-"
        links = format_html_join(
            ", ",
            '<a href="{}">{}</a>',
            (
                (
                    reverse("admin:cinema_moviereview_change", args=[review.pk]),
                    review.created_by,
                )
                for review in reviews
            ),
        )
        return links
