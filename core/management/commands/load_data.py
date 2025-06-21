import time

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Custom command to load fixtures with detailed output"

    def add_arguments(self, parser):
        # Allow the user to pass one or more fixture files as arguments
        # parser.add_argument('fixture', nargs='+', help='List of fixture files to load')
        parser.add_argument("fixture", type=str, help="List of fixture files to load")

    def handle(self, *args, **options):
        start_time = time.time()  # Start measuring time
        fixture = options["fixture"]

        self.load_fixture(fixture)

        end_time = time.time()
        elapsed_time = round(end_time - start_time, 3)

        app_label = fixture.split("/")[0]
        model_name = fixture.split("/")[-1].split(".")[0]

        self.stdout.write(
            f"Loaded model {model_name} in app {app_label} and took {elapsed_time} seconds"  # noqa: E501
        )

    def load_fixture(self, fixture):
        from io import StringIO

        out = StringIO()
        call_command("loaddata", fixture, stdout=out)

        return None
