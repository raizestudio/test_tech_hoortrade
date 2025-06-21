from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from cinema.models import Genre, Movie
from users.models import Author


class Command(BaseCommand):
    help = "Create a new movie"

    def add_arguments(self, parser):
        parser.add_argument("title", type=str, help="Title of the movie")
        parser.add_argument("release_date", type=str, help="Release date of the movie (YYYY-MM-DD)")
        parser.add_argument("author_email", type=str, help="Email of the author creating the movie")

    @atomic
    def handle(self, *args, **kwargs):
        title = kwargs["title"]
        release_date = kwargs["release_date"]
        author_email = kwargs["author_email"]

        try:
            _author = Author.objects.get(email=author_email)

        except Author.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Author with email "{author_email}" does not exist.'))
            return

        _genre = Genre.objects.get(pk=1)
        movie = Movie.objects.create(title=title, release_date=release_date, genre=_genre)
        movie.author.add(_author)
        movie.save()

        self.stdout.write(self.style.SUCCESS(f'Movie "{movie.title}" created successfully!'))
