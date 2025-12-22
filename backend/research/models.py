from form.models import UserFormSubmission
from main.models import User, MRPermission
from main.utils.permission_utils import BaseMRManager

from django.db import models

################
# Study Object #
################

class StudyManager(BaseMRManager):
    def _viewable_objects(self, user: User):
        if user.is_privacy_officer or user.is_fetc_member:
            return self.all()
        return self.filter(created_by=user)

    def _editable_objects(self, user: User):
        return self.filter(created_by=user)


class Study(models.Model):

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(
        max_length=200,
    )

    @staticmethod
    def can_be_created_by(user):
        return user.is_authenticated

    objects = StudyManager()

##########################
# Study Form Submissions #
##########################

class StudyFormSubmissionManager(BaseMRManager):

    def _viewable_objects(self, user: User):
        if user.is_privacy_officer or user.is_fetc_member:
            return self.exclude(status=Statuses.DRAFT)
        return self.filter(created_by=user)

    def _editable_objects(self, user: User):
        return self.filter(created_by=user)

class StudyFormSubmission(UserFormSubmission):
    """
    Subclass of UserFormSubmission, used specifically for submitted forms that
    relate to a specific study.
    """
    study = models.ForeignKey(Study, on_delete=models.CASCADE, related_name="form_submissions")

    @property
    def status(self,):
        return self.status_changes.last().status

########################
# Status Change Object #
########################

class Statuses(models.TextChoices):
    DRAFT = "DRA"
    SUBMITTED = "SUB"
    APPROVED = "APP"
    REJECTED = "REJ"
    REVISED = "REV"
    COMPLETED = "COM"

class StatusChange(models.Model):
    """
    Object which handles the status of a StudyFormSubmission. These are appended
    to a StudyFormSubmission as a side effect for certain actions.
    """

    status = models.CharField(
        choices=Statuses.choices
    )

    user_form_submission = models.ForeignKey(
        "research.StudyFormSubmission",
        on_delete=models.CASCADE,
        related_name="status_changes",
    )

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:

        ordering = ["created_at"]

    def __str__(self) -> str:
        return f"{Statuses(self.new_status).label}: {self.changed_time.strftime("%d-%m-%Y, %H:%M")}"
    
#################
# Review object #
#################

class ReviewRoundManager(BaseMRManager):
    def _viewable_objects(self, user: User):
        # PO and FETC members can view all reviews
        if user.is_privacy_officer or user.is_fetc_member:
            return self.all()
        # Users can see completed reviews of their own forms
        return self.filter(reviewed_form__user=user, is_active = False)

    def _editable_objects(self, user: User):
        if user.is_privacy_officer:
            return self.all()
        return self.none()

class ReviewRound(models.Model):

    reviewed_form = models.ForeignKey(
        "research.StudyFormSubmission",
        on_delete=models.CASCADE,
        related_name="review_rounds",
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    objects = ReviewRoundManager()

class Review(models.Model):

    review_form = models.ForeignKey(
        "form.UserFormSubmission",
        on_delete=models.CASCADE,
    )

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
