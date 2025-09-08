from django.conf import settings
from django.db import transaction
from django.core.management import BaseCommand, call_command, CommandError

class Command(BaseCommand):
    help = "Create dev dataset for myresearch"

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true")
        parser.add_argument("--silent", action="store_true")

    def print(self, options, *args, **kwargs):
        if not options["silent"]:
            print(*args, **kwargs)

    def _create_test_users(self, options):
        """
        Create mock users for test purposes from fixtures.
        """
        fixtures = [
            "main/management/commands/dev_fixtures/dev_users.json",
        ]

        for fixture in fixtures:
            call_command("loaddata", fixture)

    def handle(self, *args, **options):
        if not settings.DEBUG and not options["force"]:
            raise CommandError(
                "Refusing to execute command unless DEBUG = True in settings.py"
            )
        
        with transaction.atomic():
            self._create_test_users(options)
