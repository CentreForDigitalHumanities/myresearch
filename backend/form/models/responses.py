from django.db import models
from django.db.models import Min
from django.contrib.auth import get_user_model
from cdh.files.db.fields import FileField as CDHFileField
from .questions import BaseQuestion
from main.utils.permission_utils import BaseMRManager

user_model = get_user_model()
User = user_model


class MRDocument(models.Model):
    """
    An uploaded file attached to a file upload question response.
    """

    file = CDHFileField(on_delete=models.CASCADE)


class SubmissionManager(BaseMRManager):
    def _viewable_objects(self, user: User):
        if user.is_privacy_officer or user.is_fetc_member:
            return self.all()
        return self.filter(user=user)

    def _editable_objects(self, user: User):
        return self.filter(user=user)


class UserFormSubmission(models.Model):
    """Tracks a user's progress through a form."""

    user = models.ForeignKey(
        user_model, on_delete=models.CASCADE, related_name="submissions"
    )
    form = models.ForeignKey(
        "form.MRForm", on_delete=models.CASCADE, related_name="submissions"
    )
    study = models.ForeignKey(
        "research.Study",
        on_delete=models.CASCADE,
        related_name="submissions",
        null=True,
        blank=True,
    )
    started_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f"Submission {self.pk} by {self.user} started at {self.started_at.strftime('%Y-%m-%d %H:%M:%S')} (Form {self.form.pk})"

    objects = SubmissionManager()


class QuestionResponseManager(models.Manager):
    """
    Custom manager for QuestionResponses
    """

    def get_queryset(self):
        base = super().get_queryset()
        # Annotate the first submission where a response was added
        return base.annotate(first_submission_pk=Min("submissions__pk"))


class QuestionResponse(models.Model):
    """Stores a user's answer to a question."""

    objects = QuestionResponseManager()

    submissions = models.ManyToManyField(UserFormSubmission, related_name="responses")

    question = models.ForeignKey(BaseQuestion, on_delete=models.CASCADE)

    answer = models.JSONField()

    # Note that single reponses may be associated with multiple repeats. This sounds confusing,
    # but can happen when a repeatable question exists within a repeatable step.
    repeat_index = models.ForeignKey(
        "form.RepeatIndex",
        default=None,
        null=True,
        on_delete=models.CASCADE,
    )

    answered_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Response to Q{self.question.pk} in Submission {self.first_submission.pk if self.first_submission else 'unknown'}: {self.answer}"

    @property
    def first_submission(self):
        """
        Returns the submission where a response got introduced first
        """
        return self.submissions.order_by("started_at").first()
