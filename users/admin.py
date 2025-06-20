from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.html import format_html_join

from users.filters import HasMoviesFilter
from users.models import AdminUser, Author, Spectator

admin.site.register(AdminUser)


@admin.register(Author)
class AuthorAdmin(UserAdmin):
    list_display = ("email", "username", "first_name", "last_name")
    search_fields = ("email", "username")
    ordering = ("email",)
    list_filter = UserAdmin.list_filter + (HasMoviesFilter,)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "bio")}),
        ("Movies", {"fields": ("movies_list",)}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
    )
    readonly_fields = ("movies_list",)

    def movies_list(self, obj):
        movies = obj.movies.all()
        if not movies.exists():
            return "-"

        links = format_html_join(
            ", ",
            '<a href="{}">{}</a>',
            (
                (
                    reverse("admin:movies_movie_change", args=[movie.pk]),
                    movie.title,
                )
                for movie in movies
            ),
        )
        return links

    movies_list.short_description = "Movies"


admin.site.register(Spectator)
