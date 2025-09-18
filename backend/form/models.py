from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model

user_model = get_user_model()


class MRForm(models.Model):
    name = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


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
    def get_form(self) -> MRForm:
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
