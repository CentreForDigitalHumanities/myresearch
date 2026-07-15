from form.models import MRForm, BaseQuestion, QuestionResponse, UserFormSubmission
from main.models import User
from main.utils.permission_utils import BaseMRManager
from django.db import models, transaction
from django.utils import timezone
from datetime import datetime
from research.models.reviews import StatusChange, SubmissionStatus
from django.db.models import Exists, F, OuterRef, Subquery, Value, CharField, Func
from django.db.models.functions import Concat, Coalesce, Cast, Extract


class StudyManager(BaseMRManager):
    def _viewable_objects(self, user: User):
        queryset = self.filter(is_deleted=False)
        if user.is_privacy_officer or user.is_fetc_member:
            return queryset
        return queryset.filter(created_by=user)

    def _editable_objects(self, user: User):
        return self.filter(is_deleted=False, created_by=user)

    def _deletable_objects(self, user: User):
        queryset = self.filter(is_deleted=False)

        # POs and FETC members can only (soft) delete submitted studies or
        # (hard) delete their own never submitted studies
        if user.is_privacy_officer or user.is_fetc_member:
            return queryset.filter(has_been_submitted=True) | queryset.filter(
                created_by=user, has_been_submitted=False
            )
        # Normal users can only (hard) delete studies they've created, that have never been submitted
        return queryset.filter(created_by=user, has_been_submitted=False)

    def get_queryset(self):
        queryset = super().get_queryset()
        # Annotate important fields (aka question with string_id)
        queryset = self.with_answers_by_annotation_key(queryset)
        # Annotate a default title, if no title
        queryset = self.with_default_title_annotation(queryset)
        # Annotate whether the study has been submitted
        queryset = self.with_has_been_submitted_annotation(queryset)
        return queryset

    def with_has_been_submitted_annotation(self, queryset):
        """
        A study is considered submitted if it has at least one StatusChange
        whose status is not DRAFT.
        """
        return queryset.annotate(
            has_been_submitted=Exists(
                StatusChange.objects.filter(study=OuterRef("pk")).exclude(
                    status=SubmissionStatus.DRAFT
                )
            )
        )

    def with_default_title_annotation(self, queryset):
        """Override empty title values with a default based on creation date.

        Assumes title is already annotated by with_answers_by_annotation_key_annotation.
        """

        # create a default title in case there is not yet an answer to the title question
        default_title_str = Concat(
            Value("Study created on "),
            Cast(Extract("created_at", "year"), CharField()),
            Value("-"),
            # Pad with 0 on the left if month is single digit
            Func(
                Cast(Extract("created_at", "month"), CharField()),
                Value(2),
                Value("0"),
                function="LPAD",
                output_field=CharField(),
            ),
            Value("-"),
            Func(
                Cast(Extract("created_at", "day"), CharField()),
                Value(2),
                Value("0"),
                function="LPAD",
                output_field=CharField(),
            ),
            Value(" "),
            Func(
                Cast(Extract("created_at", "hour"), CharField()),
                Value(2),
                Value("0"),
                function="LPAD",
                output_field=CharField(),
            ),
            Value(":"),
            Func(
                Cast(Extract("created_at", "minute"), CharField()),
                Value(2),
                Value("0"),
                function="LPAD",
                output_field=CharField(),
            ),
            output_field=CharField(),
        )

        default_title = Func(
            default_title_str, function="to_jsonb", output_field=models.JSONField()
        )

        return queryset.annotate(
            title=Coalesce(F("title"), default_title, output_field=models.JSONField())
        )

    def with_answers_by_annotation_key(self, queryset):
        """Annotate queryset with latest answers for all questions with annotation_key.

        This is used as a default when getting a queryset in get_queryset.
        """

        # Get all questions with annotation_key that belong to forms in studies
        questions = (
            BaseQuestion.objects.filter(form__submissions__study__in=queryset)
            .filter(annotation_key__isnull=False)
            .exclude(annotation_key="")
            .distinct()
        )

        # Build annotations dictionary
        annotations = {}
        for question in questions:
            answer = (
                QuestionResponse.objects.filter(
                    submissions__study=OuterRef("id"),
                    question_id=question.id,  # type: ignore
                )
                .order_by("-submissions__started_at", "-answered_at")
                .values("answer__value")[:1]
            )

            annotations[question.annotation_key] = Subquery(answer)

        # Ensure 'title' annotation always exists
        # This ensures that default title annotation will work
        if "title" not in annotations:
            annotations["title"] = Value(None)

        # Apply annotations to queryset
        if annotations:
            queryset = queryset.annotate(**annotations)

        return queryset


class Study(models.Model):

    # A unique reference number will be created for a study upon first save()
    reference = models.CharField(max_length=10, unique=True)
    is_deleted = models.BooleanField(
        default=False,
        help_text="If true, the study is considered deleted and will not be shown in the UI.",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    # Indicate whether Study has been seen by reviewer
    is_seen = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Studies"

    objects = StudyManager()

    @staticmethod
    def can_be_created_by(user):
        return user.is_authenticated

    @property
    def form(self) -> MRForm:
        # There should only ever be one form associated with a study.
        # If there are none or more than one, we will want to know about it.
        return MRForm.objects.filter(submissions__study=self).distinct().get()

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

    @property
    def updated_at(self) -> datetime:
        return (
            UserFormSubmission.objects.filter(study=self)
            .latest("updated_at")
            .updated_at
        )

    @staticmethod
    def can_be_created_by(user):
        return user.is_authenticated

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

    def __str__(self):
        return f"Study {self.reference}"


class YearCounter(models.Model):
    """
    A helper model for generating reference numbers for studies. Keeps a counter
    for each year that gets incremented when a new Study is created.
    """

    year = models.IntegerField(unique=True)
    counter = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.year}-{self.counter}"
