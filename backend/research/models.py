from backend.research.models.reviews import SubmissionStatus
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

    @property
    def status(self):
        return self.status_changes.last().status

    objects = StudyManager()


##########################
# Study Form Submissions #
##########################


class StudyFormManager(BaseMRManager):
    def _viewable_objects(self, user: User):
        if user.is_privacy_officer or user.is_fetc_member:
            return self.exclude(status=SubmissionStatus.DRAFT)
        return self.filter(created_by=user)

    def _editable_objects(self, user: User):
        return self.filter(created_by=user)


class StudyForm(models.Model):
    """
    Ties a UserFormSubmission to a study. Used specifically for submitted forms that
    relate to a specific study.
    """

    submission = models.OneToOneField(
        UserFormSubmission,
        on_delete=models.CASCADE,
    )

    study = models.ForeignKey(Study, on_delete=models.CASCADE, related_name="forms")
