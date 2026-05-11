from django.db import models
from . import *


class BaseCondition(models.Model):
    """Abstract base class for conditions on steps or questions."""

    class ConditionType(models.TextChoices):
        SHOW = "show", "Show target"
        HIDE = "hide", "Hide target"
        REPEAT = "repeat", "Repeat target a fixed number of times"
        REPEAT_DYNAMIC = "repeat_dynamic", "Repeat based on answer value"

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

    # For (static) 'repeat' type: how many times should the target be repeated.
    repeat_count = models.PositiveIntegerField(null=True, blank=True)

    # For 'repeat_dynamic' type: use the answer to the trigger question to
    # determine how many times to repeat the target.
    use_answer_as_count = models.BooleanField(default=False)

    class Meta:
        abstract = True

    @classmethod
    def get_repeat_constraint(cls, name: str) -> models.CheckConstraint:
        """
        Returns a constraint to be used by subclasses.

        If the condition is a repeat type (either REPEAT or REPEAT_DYNAMIC),
        a repeat count should be provided or use_answer_as_count should be
        marked as true.
        """
        return models.CheckConstraint(
            check=(
                ~Q(
                    condition_type__in={
                        BaseCondition.ConditionType.REPEAT,
                        BaseCondition.ConditionType.REPEAT_DYNAMIC,
                    }
                )
                | Q(repeat_count__isnull=False)
                | Q(use_answer_as_count=True)
            ),
            name=name,
        )


class StepCondition(BaseCondition):
    """Defines when a step should be shown/hidden or repeated."""

    target_step = models.ForeignKey(
        Step,
        on_delete=models.CASCADE,
        related_name="conditions",
        help_text="The step that this condition applies to.",
    )

    class Meta:
        constraints = [
            BaseCondition.get_repeat_constraint("repeat_requires_count_or_dynamic_step")
        ]

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

    class Meta:
        constraints = [
            BaseCondition.get_repeat_constraint(
                "repeat_requires_count_or_dynamic_question"
            )
        ]

    def __str__(self):
        return f"Condition on Question {self.target_question.pk} triggered by Question {self.trigger_question.pk}"
