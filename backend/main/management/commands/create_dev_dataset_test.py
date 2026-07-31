import pytest
from typing import Type
from django.apps import apps
from django.conf import settings
from django.db.models import Model
from django.core.management import call_command

from form.models.responses import MRDocument
from research.models.reviews import Review, ReviewRound
from research.models.study import YearCounter
from form.models import (
    QuestionCondition,
    StepCondition,
    StepInfoText,
    RepeatIndex,
    Repeatable,
)

# Add models here that should be excluded from the completeness check. These
# are models that are not essential for the dev dataset or are difficult to
# generate automatically.
EXCLUDED_MODELS_FOR_COMPLETENESS_CHECK: list[Type[Model]] = [
    StepInfoText,
    StepCondition,
    QuestionCondition,
    Review,
    ReviewRound,
    YearCounter,
    RepeatIndex,
    Repeatable,
    MRDocument,
]


def test_create_dev_data(db):
    """
    Tests that the create_dev_data command runs without errors and verifies
    that test data is generated for all models in LOCAL_APPS.
    """
    try:
        call_command("create_dev_data", "--force", "--silent")
    except Exception as e:
        pytest.fail(f"Error occurred while running create_dev_data command: {e}")

    all_mr_models = [
        mr_model
        for app in settings.LOCAL_APPS
        for mr_model in apps.get_app_config(app).get_models()
    ]

    for MRModel in all_mr_models:
        if MRModel in EXCLUDED_MODELS_FOR_COMPLETENESS_CHECK:
            continue
        instances_exist = MRModel.objects.exists()
        assert instances_exist is True, (
            f"Model {MRModel.__name__} has no instances. "
            f"Please add it to the dev dataset generator or add it to "
            f"the EXCLUDED_MODELS_FOR_COMPLETENESS_CHECK list."
        )
