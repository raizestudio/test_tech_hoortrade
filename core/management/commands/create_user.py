from django.core.management import CommandError
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.db.transaction import atomic

from users.models import Author, Spectator


class Command(BaseCommand):
    help = "Create a new user with the specified username and password."

    def add_arguments(self, parser):
        parser.add_argument("email", type=str, help="The email address of the new user.")
        parser.add_argument("username", type=str, help="The username of the new user.")
        parser.add_argument("password", type=str, help="The password for the new user.")
        parser.add_argument("first_name", type=str, default="", help="The first name of the new user.")
        parser.add_argument("last_name", type=str, default="", help="The last name of the new user.")
        parser.add_argument(
            "date_of_birth", type=str, default="", help="The date of birth of the new user (optional)."
        )
        parser.add_argument(
            "--spectator", action="store_true", help="Create a spectator user instead of an author."
        )

    @atomic
    def handle(self, *args, **options):
        email = options["email"]
        username = options["username"]
        password = options["password"]
        first_name = options["first_name"]
        last_name = options["last_name"]
        date_of_birth = options["date_of_birth"]
        is_spectator = options["spectator"]

        if is_spectator:
            try:
                user = Spectator.objects.create_user(
                    email=email,
                    username=username,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    date_of_birth=date_of_birth if date_of_birth else None,
                )

            except IntegrityError:
                raise CommandError(f"Spectator with username '{username}' or email '{email}' already exists.")

        else:
            try:
                user = Author.objects.create_user(
                    email=email,
                    username=username,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    date_of_birth=date_of_birth if date_of_birth else None,
                )

            except IntegrityError:
                raise CommandError(f"Author with username '{username}' or email '{email}' already exists.")

        self.stdout.write(self.style.SUCCESS(f"User {user.username} created successfully."))
