from django.core.validators import RegexValidator, EmailValidator
from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime
from django.utils.dateparse import parse_datetime
from django.utils.safestring import mark_safe

from form.models import Repeatable

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

    step_name_override = models.BooleanField(
        default=False,
        help_text="If this is set to True, the answer to the question will "
        "override the name of its step (for stepper purposes). It can only be "
        "true for one question per step.",
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
            ),
            models.UniqueConstraint(
                fields=["step"],
                condition=models.Q(step_name_override=True),
                name="one_step_name_override_per_step",
            ),
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
            "repeatablestepquestion",
        ]:
            if hasattr(self, subclass_name):
                cls = getattr(self, subclass_name)
                if hasattr(cls, "repeatable" + subclass_name):
                    return getattr(cls, "repeatable" + subclass_name)
                return cls
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
        validator = EmailValidator(message="value must be a valid email address")
        # The email validator in the frontend is slightly different.
        if self.is_email:
            validator(answer)


class NumberQuestion(BaseQuestion):
    positive_only = models.BooleanField(default=False)

    def validate(self, answer: str):
        super().validate(answer)
        value = int(answer)
        if self.positive_only and value < 0:
            raise ValueError("value in must be positive")


class DateQuestion(BaseQuestion):
    future_only = models.BooleanField(default=False)

    def validate(self, answer: str):
        super().validate(answer)
        value = parse_datetime(answer)
        if self.future_only and value and datetime.now() > value:
            raise ValueError("value must be in the future")


class FileUploadQuestion(BaseQuestion):
    size_limit = models.PositiveIntegerField(help_text="Maximum file size in bytes.")


class RepeatableStepQuestion(BaseQuestion):
    """
    A special question, with which repeatable steps can be created, deleted and managed.

    Does not have a response, but is used to trigger mutations.
    """

    repeatable_step = models.OneToOneField(
        "form.RepeatableStep", on_delete=models.CASCADE
    )

    create_text = models.CharField()

    none_yet_text = models.CharField()


class RepeatableTextQuestion(
    Repeatable,
    TextQuestion,
):
    pass
