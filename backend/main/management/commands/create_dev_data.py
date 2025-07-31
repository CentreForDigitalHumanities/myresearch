from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.db import transaction
from django.apps import apps

from main.models import User


class Command(BaseCommand):
    help = "Create dev dataset for myresearch"

    # All models for which dev data has been implemented. Add the model to
    # this list when dev data creation has been implemented for this model.
    dev_data_models = [
        User,
    ]

    def print(self, options, *args, **kwargs):
        if not options["silent"]:
            print(*args, **kwargs)

    def handle(self, *args, **options):
        if not settings.DEBUG and not options["force"]:
            raise CommandError(
                "Refusing to execute command unless DEBUG = True in settings.py"
            )

        self._check_all_models_implemented()

        with transaction.atomic():
            self._create_test_users(options)

    def _create_test_users(self, options):
        """
        Create mock users for test purposes from fixtures.
        """
        fixtures = [
            "main/management/commands/dev_fixtures/dev_users.json",
        ]

        for fixture in fixtures:
            call_command("loaddata", fixture)

    def _check_all_models_implemented(
        self,
    ):
        """
        Gather all models from LOCAL_APPS and check if they are all present in
        dev_data_models.
        """

        all_mr_models = []

        for app in settings.LOCAL_APPS:
            for mr_model in apps.get_app_config(app).get_models():
                all_mr_models.append(mr_model)

        for mr_model in all_mr_models:
            if mr_model not in self.dev_data_models:
                raise CommandError(
                    f"The model {mr_model} is not yet represented in the dev "
                    "data creation."
                )
