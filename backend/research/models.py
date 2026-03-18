from research.other_models.utils import YearCounter
from research.other_models.reviews import SubmissionStatus
from form.models import UserFormSubmission
from main.models import User, MRPermission
from main.utils.permission_utils import BaseMRManager

from django.db import models, transaction
from django.utils import timezone

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

    reference = models.CharField(max_length=10, unique=True, blank=True)

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

    def save(self, *args, **kwargs):

        if not self.reference:
            with transaction.atomic():
                year = timezone.now().year % 100  # 2026 -> 26

                counter_obj, _ = YearCounter.objects.select_for_update().get_or_create(
                    year=year
                )

                counter_obj.counter += 1
                counter_obj.save()

                self.reference = f"MR-{year:02d}-{counter_obj.counter:04d}"

        super().save(*args, **kwargs)
