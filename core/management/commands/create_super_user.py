from users.models import AdminUser
from django.core.management import CommandError
from django.core.management.base import BaseCommand
from django.db.transaction import atomic


class Command(BaseCommand):
    help = "Create a superuser"

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument("email", type=str, help="Email for the superuser")
        parser.add_argument("username", type=str, help="Username for the superuser")
        parser.add_argument("password", type=str, help="Password for the superuser")

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Creating superuser..."))

        if not options.get("email"):
            raise CommandError("The --email option is required.")

        if not options.get("username"):
            raise CommandError("The --username option is required.")

        if not options.get("password"):
            raise CommandError("The --password option is required.")

        with atomic():
            _user = AdminUser.objects.create_superuser(
                username=options["username"],
                email=options["email"],
                password=options["password"],
            )
            _user.is_superuser = True
            _user.is_staff = True
            _user.is_admin = True
            _user.save()

        self.stdout.write(self.style.SUCCESS(f"Superuser created successfully: {options['username']}"))
