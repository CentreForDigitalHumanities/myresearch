from django.db import models
from django.db.models import Q, Min, QuerySet
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .responses import UserFormSubmission
from .questions import BaseQuestion

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

    # Automatically set to the top-level form this step belongs to
    top_form = models.ForeignKey(
        MRForm,
        on_delete=models.CASCADE,
        related_name="all_steps",
        null=True,
        blank=True,
        editable=False,
    )

    is_overview = models.BooleanField(
        default=False,
        help_text="If true, this step serves as an overview step for the entire form. It should not have any questions attached to it.",
    )

    class Meta:
        order_with_respect_to = "parent"

    def clean(self) -> None:
        """Validate that overview steps don't have questions."""
        super().clean()
        if self.is_overview and self.pk and self.questions.exists():  # type: ignore
            raise ValidationError(
                {
                    "is_overview": "Cannot mark as overview step when questions are attached."
                }
            )

    def save(self, *args, **kwargs):
        """Automatically set the top_form based on the form or parent relationship."""
        # Validate the constraint: either form or parent must be set, but not both
        if (self.form is None and self.parent is None) or (
            self.form is not None and self.parent is not None
        ):
            raise ValueError(
                "Step must have either 'form' (for top-level steps) or 'parent' (for substeps), but not both."
            )

        if self.form:
            self.top_form = self.form
        else:
            parent = self.parent
            while not parent.form_id:
                parent = parent.parent
            self.top_form_id = parent.form_id

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.pk})"


class StepInfoText(models.Model):
    step = models.OneToOneField(
        Step, on_delete=models.CASCADE, related_name="info_text"
    )
    text = models.TextField()
