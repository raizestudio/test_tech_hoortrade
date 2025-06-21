import hashlib

import requests
from django.conf import settings
from django.core.cache import cache
from django.core.management.base import BaseCommand

from cinema.models import Movie
from core.models import DataSource


class Command(BaseCommand):
    help = "Search and import movies from TMDB."

    def add_arguments(self, parser):
        parser.add_argument("query", type=str, help="Search term for TMDB")
        parser.add_argument("--page", type=int, default=1, help="Page number")
        parser.add_argument("--include-adult", action="store_true", help="Include adult content")

    def handle(self, *args, **options):
        query = options["query"]
        page = options["page"]
        include_adult = options["include_adult"]

        # Generate a stable cache key
        key_raw = f"tmdb:search:{query}:{page}:{include_adult}"
        cache_key = "tmdb:" + hashlib.sha256(key_raw.encode()).hexdigest()
        results = cache.get(cache_key)

        if results is None:
            url = "https://api.themoviedb.org/3/search/movie"
            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {settings.TMDB_API_KEY}",
            }
            params = {"query": query, "page": page, "include_adult": include_adult, "language": "en-US"}

            response = requests.get(url, headers=headers, params=params)
            if response.status_code != 200:
                self.stderr.write(self.style.ERROR("TMDB API error"))
                return

            results = response.json().get("results", [])
            cache.set(cache_key, results, timeout=60 * 15)  # Cache for 15 minutes

            self.stdout.write(self.style.NOTICE("Fetched from TMDB API."))
        else:
            self.stdout.write(self.style.NOTICE("Loaded from cache."))

        if not results:
            self.stdout.write(self.style.WARNING("No results found."))
            return

        for i, movie in enumerate(results):
            title = movie.get("title")
            release_date = movie.get("release_date", "N/A")
            lang = movie.get("original_language", "")
            print(f"{i + 1}. {title} ({release_date}) [{lang}]")

        selected = input("\nEnter the numbers of movies to import (comma-separated): ")
        try:
            indexes = [int(i.strip()) - 1 for i in selected.split(",")]
        except ValueError:
            self.stderr.write(self.style.ERROR("Invalid input. Use comma-separated numbers."))
            return

        for i in indexes:
            if 0 <= i < len(results):
                movie_data = results[i]
                movie, created = Movie.objects.get_or_create(
                    title=movie_data.get("title"),
                    original_title=movie_data.get("original_title"),
                    release_date=movie_data.get("release_date") or None,
                    defaults={
                        "description": movie_data.get("overview", ""),
                        "original_language": movie_data.get("original_language"),
                        "status": "RELEASED" if movie_data.get("release_date") else "DRAFT",
                        "adult_content": movie_data.get("adult", False),
                        "poster": None,  # TODO: Handle poster image
                        "source": DataSource.TMDB.name,
                    },
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"✔ Added: {movie.title}"))
                else:
                    self.stdout.write(self.style.WARNING(f"✘ Skipped (already exists): {movie.title}"))
            else:
                self.stderr.write(self.style.ERROR(f"Invalid index: {i + 1}"))
