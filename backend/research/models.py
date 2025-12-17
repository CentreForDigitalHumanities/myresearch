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

#######################
# Staus Change Object #
#######################

class Statuses(models.TextChoices):
    CREATED = "CRE"
    SUBMITTED = "SUB"
    APPROVED = "APP"
    REJECTED = "REJ"
    REVISED = "REV"
    COMPLETED = "COM"

class StatusChange(models.Model):

    status = models.CharField(
        choices=Statuses.choices
    )

    # Not currently in this branch

    # user_form_submission = models.ForeignKey(
    #     "form.UserFormSubmission",
    #     on_delete=models.CASCADE,
    #     related_name="status_changes",
    # )

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{Statuses(self.new_status).label}: {self.changed_time.strftime("%d-%m-%Y, %H:%M")}" 