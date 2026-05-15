from research.other_models.reviews import StatusChange, SubmissionStatus
from research.other_models.utils import YearCounter
from form.models import UserFormSubmission
from main.models import User
from form.models import MRForm, QuestionResponse, UserFormSubmission
from main.models import User
from main.utils.permission_utils import BaseMRManager

from django.db import models, transaction
from django.utils import timezone


class StudyManager(BaseMRManager):
    def _viewable_objects(self, user: User):
        if user.is_privacy_officer or user.is_fetc_member:
            return self.all()
        return self.filter(created_by=user)

    def _editable_objects(self, user: User):
        return self.filter(created_by=user)


class Study(models.Model):

    # A unique reference number will be created for a study upon first save()
    reference = models.CharField(max_length=10, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    @staticmethod
    def can_be_created_by(user):
        return user.is_authenticated

    @property
    def form(self) -> MRForm:
        # There should only ever be one form associated with a study.
        # If there are none or more than one, we will want to know about it.
        return MRForm.objects.filter(submissions__study=self).distinct().get()

    @property
    def name(self) -> str:
        default_name = (
            f"Study created on {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
        )

        name_question = self.form.study_name_question
        if name_question is None:
            return default_name

        try:
            submission = UserFormSubmission.objects.get(
                user=self.created_by,
                form=self.form,
                study=self,
            )
            response = QuestionResponse.objects.filter(
                submissions=submission,
                question_id=name_question.id,
            ).latest("answered_at")
            return (
                response.answer["value"]
                if response and response.answer
                else default_name
            )
        except Exception as e:
            return default_name

    @property
    def status(self) -> SubmissionStatus:
        """
        Returns the current status of the study, as determined by the latest
        StatusChange. If none can be found, DRAFT is used as a default.
        """
        last_status_change = (
            StatusChange.objects.filter(study=self).order_by("created_at").last()
        )
        return (
            SubmissionStatus(last_status_change.status)
            if last_status_change
            else SubmissionStatus.DRAFT
        )

    class Meta:
        verbose_name_plural = "Studies"

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
