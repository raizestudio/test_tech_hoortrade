from django.contrib import admin

from users.models import Author


class HasMoviesFilter(admin.SimpleListFilter):
    title = "Has Movies"
    parameter_name = "has_movies"

    def lookups(self, request, model_admin):
        return (
            ("yes", "Yes"),
            ("no", "No"),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return Author.objects.get_authors_with_atleast_one_movie()
        elif self.value() == "no":
            return queryset.exclude(pk__in=Author.objects.get_authors_with_atleast_one_movie())
        return queryset
