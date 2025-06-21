from django.core.management.base import BaseCommand
from tqdm import tqdm

from cinema.tests.factories.factory_movie import MovieFactory
from core.models import DataSource


class Command(BaseCommand):
    help = "Generate fake movies"

    def add_arguments(self, parser):
        parser.add_argument("count", type=int, help="Number of fake movies to create")

    def handle(self, *args, **options):
        count = options["count"]
        self.stdout.write(f"Creating {count} fake movie(s)...\n")

        for _ in tqdm(range(count), desc="Generating movies", unit="movie"):
            MovieFactory(source=DataSource.CMD.name)

        self.stdout.write(self.style.SUCCESS(f"Successfully created {count} fake movie(s)."))
