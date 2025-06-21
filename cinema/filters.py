from django.contrib.admin import SimpleListFilter


class AverageRatingFilter(SimpleListFilter):
    title = "average rating"
    parameter_name = "average_rating_range"

    def lookups(self, request, model_admin):
        return [
            ("<2", "Less than 2"),
            ("2-3", "2 to 3"),
            ("3-4", "3 to 4"),
            ("4-5", "4 to 5"),
            ("5", "Exactly 5"),
        ]

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset

        filtered_ids = []

        for movie in queryset:
            avg = movie.average_rating
            if avg is None:
                continue
            if self.value() == "<2" and avg < 2:
                filtered_ids.append(movie.id)
            elif self.value() == "2-3" and 2 <= avg < 3:
                filtered_ids.append(movie.id)
            elif self.value() == "3-4" and 3 <= avg < 4:
                filtered_ids.append(movie.id)
            elif self.value() == "4-5" and 4 <= avg < 5:
                filtered_ids.append(movie.id)
            elif self.value() == "5" and avg == 5:
                filtered_ids.append(movie.id)

        return queryset.filter(id__in=filtered_ids)
