from django.core.management import CommandError
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from users.models import Author, Spectator


class Command(BaseCommand):
    help = "Create a new user with the specified username and password."

    def add_arguments(self, parser):
        parser.add_argument("email", type=str, help="The email address of the new user.")
        parser.add_argument("username", type=str, help="The username of the new user.")
        parser.add_argument("password", type=str, help="The password for the new user.")
        parser.add_argument(
            "--spectator", action="store_true", help="Create a spectator user instead of an author."
        )

    @atomic
    def handle(self, *args, **options):
        email = options["email"]
        username = options["username"]
        password = options["password"]
        is_spectator = options["spectator"]

        if not email or not username or not password:
            raise CommandError("Email, username, and password are required.")

        if is_spectator:
            user = Spectator.objects.create_user(
                email=email,
                username=username,
                password=password,
            )

        else:
            user = Author.objects.create_user(
                email=email,
                username=username,
                password=password,
            )

        self.stdout.write(self.style.SUCCESS(f"User {user.username} created successfully."))
