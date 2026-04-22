from django.db import models
from django.db.models import Q, Min, QuerySet
from django.contrib.auth import get_user_model
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

    def all_steps(self) -> list["Step"]:
        """
        Get all steps and substeps from a form as a flat list, up to an arbitrary depth.
        """
        all_steps_list = []
        stack: list["Step"] = list(self.steps.all())  # type: ignore

        while stack:
            step = stack.pop()
            all_steps_list.append(step)
            # Add substeps to the stack to process them
            stack.extend(step.substeps.all())  # type: ignore

        return all_steps_list

    def all_questions(self) -> list:
        """
        Get all questions from a form as a flat list, up to an arbitrary depth.
        Returns specific question subclass instances (TextQuestion, SelectQuestion, etc.)
        """
        all_questions_list = []
        for step in self.all_steps():
            questions: QuerySet[BaseQuestion] = step.questions.all()  # type: ignore
            for question in questions:
                all_questions_list.append(question.get_subclass())
        return all_questions_list

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


class StepInfoText(models.Model):
    step = models.OneToOneField(
        Step, on_delete=models.CASCADE, related_name="info_text"
    )
    text = models.TextField()
