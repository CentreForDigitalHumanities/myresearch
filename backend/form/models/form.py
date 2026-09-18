from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

user_model = get_user_model()


class MRForm(models.Model):
    name = models.CharField(max_length=200)
    version = models.CharField(max_length=10, help_text="E.g. 1.0.0, 2.15.3")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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

    form = models.ForeignKey(
        MRForm,
        on_delete=models.CASCADE,
        related_name="steps",
    )

    # Only for substeps.
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="substeps",
        null=True,
        blank=True,
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

    def __str__(self):
        return f"{self.name} ({self.pk})"


class StepInfoText(models.Model):
    step = models.ForeignKey(
        Step, on_delete=models.CASCADE, related_name="step_info_texts"
    )
    text = models.CharField(max_length=200)
    content = models.TextField()

    class Meta:
        order_with_respect_to = "step"


class RepeatIndex(models.Model):
    """
    A marker for various repeatable items to be connected
    to a UserFormSubmission through a ManyToMany relationship.

    Although a repeatable item has a simple relationship to
    its indices representing its repeats, the index itself has
    an additional relationship to its parent. This is necessary
    to disambiguate parallel nested repeats within the same
    submission.
    """

    parent = models.ForeignKey(
        to="form.RepeatIndex",
        on_delete=models.CASCADE,
        default=None,
        null=True,
        related_name="children",
    )

    submissions = models.ManyToManyField(
        to="form.UserFormSubmission",
        related_name="repeats",
    )


class Repeatable(models.Model):
    repeat_indices = models.ManyToManyField(to=RepeatIndex)

    class Meta:
        abstract = True


class RepeatableStep(Repeatable, Step):
    pass
