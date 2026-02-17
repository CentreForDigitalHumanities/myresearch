from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model

user_model = get_user_model()


class MRForm(models.Model):
    name = models.CharField(max_length=200)
    version = models.CharField(max_length=10, help_text="E.g. 1.0.0, 2.15.3")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    study_name_question = models.ForeignKey(
        "form.BaseQuestion",
        on_delete=models.SET_NULL,
        related_name="study_name_forms",
        help_text="If set, the answer to this question will be used as the study name.",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Form"
        verbose_name_plural = "Forms"

    def __str__(self):
        return f"{self.name} ({self.pk})"


class Step(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(
        max_length=200,
        unique=True,
        help_text="Used in the URL.",
    )

    # Only for the top-level steps.
    form = models.ForeignKey(
        MRForm,
        on_delete=models.CASCADE,
        related_name="steps",
        null=True,
        blank=True,
    )

    # Only for substeps.
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="substeps",
        null=True,
        blank=True,
    )

    class Meta:
        order_with_respect_to = "parent"
        constraints = [
            models.CheckConstraint(
                # Parent and form cannot both be set, but one of them must be.
                check=(
                    Q(parent__isnull=True, form__isnull=False)
                    | Q(parent__isnull=False, form__isnull=True)
                ),
                name="step_parent_xor_form",
            )
        ]

    @property
    def top_form(self) -> MRForm:
        """Returns the MRForm this step belongs to, whether directly or indirectly."""

        def _get_form_recursive(step: Step, visited: set[int]) -> MRForm:
            """Helper method to recursively find the MRForm, tracking visited steps to avoid infinite loops."""

            if step.pk is None:
                raise ValueError("Step must be saved before calling get_form.")

            if step.pk in visited:
                raise ValueError("Circular reference detected in step hierarchy.")
            visited.add(step.pk)

            if step.form:
                return step.form
            elif step.parent:
                return _get_form_recursive(step.parent, visited)
            else:
                # This should never happen.
                raise ValueError("Step is neither a top-level step nor a substep.")

        return _get_form_recursive(self, set())

    def __str__(self):
        return f"{self.name} ({self.pk})"


class StepInfoQuestion(models.Model):
    step = models.ForeignKey(
        Step, on_delete=models.CASCADE, related_name="info_questions"
    )
    text = models.CharField(max_length=200)
    link = models.URLField(max_length=200)


class StepInfoText(models.Model):
    step = models.ForeignKey(Step, on_delete=models.CASCADE, related_name="info_texts")
    text = models.TextField()


# Questions
class BaseQuestion(models.Model):
    text = models.CharField(max_length=200)
    step = models.ForeignKey(Step, on_delete=models.CASCADE, related_name="questions")
    description = models.TextField(
        blank=True,
        help_text="Context about the question and its purpose, which will be shown to the user.",
    )
    required = models.BooleanField(default=False)

    class Meta:
        order_with_respect_to = "step"

    def __str__(self):
        return f"{self.text} ({self.pk})"


class SelectQuestion(BaseQuestion):
    multiple = models.BooleanField(
        default=False,
        help_text="Allows multiple options to be selected if true.",
    )


class SelectOption(models.Model):
    label = models.CharField(max_length=200)
    default_selected = models.BooleanField(default=False)
    question = models.ForeignKey(
        SelectQuestion, on_delete=models.CASCADE, related_name="options"
    )


class TrueFalseQuestion(BaseQuestion):
    default_value = models.BooleanField(default=False)


class TextQuestion(BaseQuestion):
    placeholder = models.CharField(max_length=200, blank=True)
    lines = models.PositiveIntegerField(default=1)


class NumberQuestion(BaseQuestion):
    positive_only = models.BooleanField(default=False)


class DateQuestion(BaseQuestion):
    future_only = models.BooleanField(default=False)


class FileUploadQuestion(BaseQuestion):
    size_limit = models.PositiveIntegerField()


# User responses / answers
class UserFormSubmission(models.Model):
    """Tracks a user's progress through a form."""

    user = models.ForeignKey(user_model, on_delete=models.CASCADE)
    form = models.ForeignKey(MRForm, on_delete=models.CASCADE)
    study = models.ForeignKey(
        "research.Study", on_delete=models.CASCADE, related_name="forms", null=True
    )
    started_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f"Submission {self.pk} by {self.user} started at {self.started_at.strftime('%Y-%m-%d %H:%M:%S')} (Form {self.form.pk})"


class QuestionResponse(models.Model):
    """Stores a user's answer to a question."""

    submission = models.ForeignKey(
        UserFormSubmission, on_delete=models.CASCADE, related_name="responses"
    )
    question = models.ForeignKey(BaseQuestion, on_delete=models.CASCADE)

    answer = models.JSONField()

    # For repeated questions/steps, track which instance this is
    # 0 = first instance, 1 = second, etc.
    repeat_index = models.PositiveIntegerField(
        default=0, help_text="Index for repeated questions."
    )

    answered_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["submission", "question", "repeat_index"]

    def __str__(self):
        return f"Response to Q{self.question.pk} in Submission {self.submission.pk}"


# Conditional logic for questions and steps
class BaseCondition(models.Model):
    """Abstract base class for conditions on steps or questions."""

    class ConditionType(models.TextChoices):
        SHOW = "show", "Show target"
        HIDE = "hide", "Hide target"
        REPEAT = "repeat", "Repeat target a fixed number of times"
        REPEAT_DYNAMIC = "repeat_dynamic", "Repeat based on answer value"

    class TriggerValueKeys(models.TextChoices):
        VALUE = "value", "Value"
        OPTION_IDS = "option_ids", "Option IDs"
        MIN = "min", "Minimum"
        MAX = "max", "Maximum"
        EXACT = "exact", "Exact"

    trigger_question = models.ForeignKey(
        BaseQuestion,
        on_delete=models.CASCADE,
        help_text="The question whose answer triggers this condition.",
    )

    condition_type = models.CharField(
        max_length=20,
        choices=ConditionType.choices,
    )

    # Check out form/README.md for more information on how to format this field.
    trigger_value = models.JSONField()

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

        You cannot define constraints on abstract base classes, so
        subclasses should call this method to get the constraint to add
        to their Meta.constraints.
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

    trigger_question = models.ForeignKey(
        BaseQuestion,
        on_delete=models.CASCADE,
        related_name="triggered_step_conditions",
        help_text="The question whose answer triggers this condition.",
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

    trigger_question = models.ForeignKey(
        BaseQuestion,
        on_delete=models.CASCADE,
        related_name="triggered_conditions",
        help_text="The question whose answer triggers this condition.",
    )

    class Meta:
        constraints = [
            BaseCondition.get_repeat_constraint(
                "repeat_requires_count_or_dynamic_question"
            )
        ]

    def __str__(self):
        return f"Condition on Question {self.target_question.pk} triggered by Question {self.trigger_question.pk}"
