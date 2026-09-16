from django.db import models
from django.db.models import Q
from . import *


class BaseCondition(models.Model):
    """Abstract base class for conditions on steps or questions."""

    class ConditionType(models.TextChoices):
        SHOW = "show", "Show target"
        HIDE = "hide", "Hide target"

    class TriggerValueKeys(models.TextChoices):
        VALUE = "value", "Value"
        MIN = "min", "Minimum"
        MAX = "max", "Maximum"
        EXACT = "exact", "Exact"

    trigger_question = models.ForeignKey(
        BaseQuestion,
        on_delete=models.CASCADE,
        help_text="The question whose answer triggers this condition.",
        related_name="triggered_%(class)s",
    )

    condition_type = models.CharField(
        max_length=20,
        choices=ConditionType.choices,
    )

    # Check out form/README.md for more information on how to format this field.
    # blank=True is necessary to ensure {} is correctly accepted as valid JSON.
    trigger_value = models.JSONField(blank=True)

    class Meta:
        abstract = True


class StepCondition(BaseCondition):
    """Defines when a step should be shown/hidden or repeated."""

    target_step = models.ForeignKey(
        Step,
        on_delete=models.CASCADE,
        related_name="conditions",
        help_text="The step that this condition applies to.",
    )

    def __str__(self):
        return f"Condition on Step {self.target_step.pk} triggered by Question {self.trigger_question.pk}"


class QuestionCondition(BaseCondition):
    """Defines when a question should be shown/hidden or repeated."""

    target_question = models.ForeignKey(
        BaseQuestion,
        on_delete=models.CASCADE,
        related_name="conditions",
        help_text="The question that this condition applies to.",
    )

    def __str__(self):
        return f"Condition on Question {self.target_question.pk} triggered by Question {self.trigger_question.pk}"
