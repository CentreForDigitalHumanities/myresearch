from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command

from django.conf import settings


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true")

    def handle(self, *args, **options):
        if not settings.DEBUG and not options["force"]:
            raise CommandError(
                "Refusing to execute command unless DEBUG = True in settings.py"
            )

        self._load_test_users(options)
        self._load_vwr_form(options)

    def _load_test_users(self, options):
        """
        Create mock users for test purposes from fixtures.

        NOTE: These users are the same as the ones provided by the
        Dev-IDP and must be kept the same!
        """
        fixtures = [
            "main/management/commands/dev_fixtures/dev_users.json",
        ]

        for fixture in fixtures:
            call_command("loaddata", fixture)
            print("Dev users loaded.")

    def _load_vwr_form(self, options):
        """
        Loads the vwr form from a fixture
        """

        fixtures = ["form/fixtures/vwr.json"]

        for fixture in fixtures:
            call_command("loaddata", fixture)
            print("ProcReg Form fixture loaded.")
