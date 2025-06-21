from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

AVAILABLE_FIXTURES = ("cinema.genre",)

ENVS = [
    "dev",
    "prod",
]


class Command(BaseCommand):

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument("--env", type=str, help="Environment to load fixtures for")

    def handle(self, *args, **options):
        self.stdout.write("Loading fixtures...")
        env = options.get("env", "dev")
        if env not in ENVS:
            env = "dev"

        self.stdout.write(f"Environment: {env}")
        for fixture in AVAILABLE_FIXTURES:
            try:
                app_label, model_name = fixture.split(".")
                call_command("load_data", f"{app_label}/fixtures/{env}/{model_name}.json")
            except CommandError as e:
                self.stdout.write(f"Error loading {fixture}: {e}")
            except Exception as e:
                self.stdout.write(f"Error loading {fixture}: {e}")
