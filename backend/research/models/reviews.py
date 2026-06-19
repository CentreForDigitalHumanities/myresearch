from django.db import models

from main.models import User
from main.utils.permission_utils import BaseMRManager


class SubmissionStatus(models.TextChoices):
    # NOTE: These names need to be identical in order for codegen
    # to generate these correctly for the frontend
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class StatusChangeManager(BaseMRManager):
    def _viewable_objects(self, user: User):
        if user.is_privacy_officer or user.is_fetc_member:
            return self.all()
        return self.filter(created_by=user)

    def _editable_objects(self, user: User):
        pass

class StatusChange(models.Model):
    """
    Object which handles the status of a Study. These are appended
    to a Study as a side effect for certain actions.
    """

    status = models.CharField(choices=SubmissionStatus.choices)

    study = models.ForeignKey(
        "research.Study",
        on_delete=models.CASCADE,
        related_name="status_changes",
    )

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = StatusChangeManager()

    class Meta:
        ordering = ["created_at"]


    def __str__(self) -> str:
        return f"{SubmissionStatus(self.status).label}: {self.created_at.strftime('%d-%m-%Y, %H:%M')}"


class ReviewRoundManager(BaseMRManager):
    def _viewable_objects(self, user: User):
        # PO and FETC members can view all reviews
        if user.is_privacy_officer or user.is_fetc_member:
            return self.all()
        # Users can see completed reviews of their own forms
        return self.filter(reviewed_form__user=user, is_active=False)

    def _editable_objects(self, user: User):
        if user.is_privacy_officer:
            return self.all()
        return self.none()


class ReviewRound(models.Model):

    reviewed_form = models.OneToOneField(
        "form.UserFormSubmission",
        on_delete=models.CASCADE,
        related_name="review_round",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    feedback = models.TextField()

    class Meta:
        ordering = ["created_at"]

    objects = ReviewRoundManager()


class ReviewVerdict(models.TextChoices):
    APPROVED = "APP"
    REJECTED = "REJ"


class Review(models.Model):

    round = models.ForeignKey(
        ReviewRound,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    comments = models.TextField()

    verdict = models.CharField(choices=ReviewVerdict.choices)
