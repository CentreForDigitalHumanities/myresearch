from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.core.exceptions import ValidationError

from django.utils.safestring import mark_safe

snake_case_validator = RegexValidator(
    regex=r"^[a-z]+(_[a-z]+)*$",
    message="Only snake_case is allowed (e.g. 'recording_details'). Read help text carefully!",
)


class BaseQuestion(models.Model):

    annotation_key = models.CharField(
        blank=True,
        null=True,
        help_text=mark_safe(
            "<strong>Only for important questions! When in doubt, leave this "
            "blank!</strong> If needed, provide a short, descriptive name in "
            "snake_case, eg. 'recording_details'. This is used for annotating "
            "the answers to certain question from a submission to the "
            "corresponding Study, which can be useful for list filters."
        ),
        validators=[snake_case_validator],
    )

    text = models.CharField(max_length=200)
    step = models.ForeignKey(
        "form.Step", on_delete=models.CASCADE, related_name="questions"
    )
    # synced from step.form on save
    form = models.ForeignKey(
        "form.MRForm",
        on_delete=models.CASCADE,
        related_name="questions",
        editable=False,
    )
    description = models.TextField(
        blank=True,
        help_text="Context about the question and its purpose, which will be shown to the user.",
    )
    required = models.BooleanField(default=False)

    class Meta:
        order_with_respect_to = "step"
        constraints = [
            models.UniqueConstraint(
                fields=["form", "annotation_key"],
                name="unique_annotation_key_per_form",
                condition=models.Q(annotation_key__isnull=False),
            )
        ]

    @property
    def has_conditions(self) -> bool:
        """
        Returns True if there are any step or question conditions dependent on
        this question.
        """
        return (
            self.triggered_questioncondition.exists()  # type: ignore
            or self.triggered_stepcondition.exists()  # type: ignore
        )

    def clean(self) -> None:
        """Validate that questions are not attached to overview steps."""
        super().clean()
        if self.pk and self.step.is_overview:
            raise ValidationError(
                {"step": "Questions cannot be attached to overview steps."}
            )

    def save(self, *args, **kwargs):
        """Run full clean and sync top_form from step, to ensure validators get run."""
        # Sync form from the step's top_form
        if self.step and self.step.form:
            self.form = self.step.form
        self.full_clean()
        super().save(*args, **kwargs)

    def validate(self, answer: str):
        pass

    def get_subclass(self):
        """
        Returns the actual subclass instance (TextQuestion, SelectQuestion, etc.).
        BaseQuestion is used as a fallback.
        """
        for subclass_name in [
            "selectquestion",
            "truefalsequestion",
            "textquestion",
            "numberquestion",
            "datequestion",
            "fileuploadquestion",
        ]:
            if hasattr(self, subclass_name):
                return getattr(self, subclass_name)
        return self

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

    class Meta:
        order_with_respect_to = "question"


class TrueFalseQuestion(BaseQuestion):
    default_value = models.BooleanField(default=False)


class TextQuestion(BaseQuestion):
    placeholder = models.CharField(max_length=200, blank=True)
    lines = models.PositiveIntegerField(default=1)
    is_email = models.BooleanField(default=False)

    def validate(self, answer: str):
        super().validate(answer)


class NumberQuestion(BaseQuestion):
    positive_only = models.BooleanField(default=False)

    def validate(self, answer: str):
        super().validate(answer)
        value = int(answer)
        if value < 0 and self.positive_only:
            raise ValueError("value in must be positive")

class DateQuestion(BaseQuestion):
    future_only = models.BooleanField(default=False)


class FileUploadQuestion(BaseQuestion):
    size_limit = models.PositiveIntegerField()
