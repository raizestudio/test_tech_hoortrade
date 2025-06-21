from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.db.transaction import atomic

from cinema.models import Genre, Movie
from core.models import DataSource
from users.models import Author


class Command(BaseCommand):
    help = "Create a new movie"

    def add_arguments(self, parser):
        parser.add_argument("title", type=str, help="Title of the movie")
        parser.add_argument("original_title", type=str, help="Original title of the movie")
        parser.add_argument("release_date", type=str, help="Release date of the movie (YYYY-MM-DD)")
        parser.add_argument("author_email", type=str, help="Email of the author creating the movie")

    @atomic
    def handle(self, *args, **kwargs):
        title = kwargs["title"]
        original_title = kwargs["original_title"]
        release_date = kwargs["release_date"]
        author_email = kwargs["author_email"]

        try:
            _author = Author.objects.get(email=author_email)

        except Author.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Author with email "{author_email}" does not exist.'))
            return

        _genre = Genre.objects.get(pk=1)

        try:
            movie = Movie.objects.create(
                title=title,
                original_title=original_title,
                release_date=release_date,
                source=DataSource.CMD.name,
            )
            movie.genres.add(_genre)
            movie.authors.add(_author)
            movie.save()

            self.stdout.write(self.style.SUCCESS(f'Movie "{movie.title}" created successfully!'))

        except IntegrityError:
            self.stdout.write(
                self.style.ERROR(
                    f'A movie with title "{title}" and release date {release_date} already exists.'
                )
            )
