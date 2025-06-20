from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html_join

from movies.models import Genre, Movie, MovieReview, AuthorReview

admin.site.register(Genre)
admin.site.register(MovieReview)
admin.site.register(AuthorReview)

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "release_date",
        "rating",
        "status",
        # "genres",
    )
    search_fields = ("title", "description")
    list_filter = ("status", "release_date")
    ordering = ("-release_date",)

    fieldsets = (
        (None, {"fields": ("title", "description", "release_date", "rating", "status", "reviews_list")}),
        ("Genre and Author", {"fields": ("genre", "authors_list")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )
    readonly_fields = ("created_at", "updated_at", "authors_list", "reviews_list")

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
                    reverse("admin:movies_moviereview_change", args=[review.pk]),
                    review.created_by,
                )
                for review in reviews
            ),
        )
        return links
