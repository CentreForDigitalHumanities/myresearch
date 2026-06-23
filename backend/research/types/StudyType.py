from django.db.models import OuterRef, QuerySet, Q, Subquery
from graphene import ID, Enum, List, NonNull, ResolveInfo, String, Field
from django_filters import FilterSet, ModelMultipleChoiceFilter, MultipleChoiceFilter
from datetime import datetime
from api.gql_list_object_type import GQLListObjectType
from form.models.questions import SelectOption
from form.models import UserFormSubmission
from research.models.study import Study
from research.models.reviews import StatusChange, SubmissionStatus
from research.utils.study_actions import ActionEnum, StudyActions

GQLSubmissionStatus = Enum.from_enum(SubmissionStatus)


class StudyFilter(FilterSet):

    statuses = MultipleChoiceFilter(
        field_name="status",
        method="filter_latest_status",
        choices=SubmissionStatus.choices[:2],
    )

    faculties = ModelMultipleChoiceFilter(
        field_name="faculty",
        queryset=SelectOption.objects.filter(question__annotation_key="faculty"),
        method="filter_faculties",
    )

    def filter_latest_status(self, queryset, name, value):
        """Filter studies by their latest StatusChange status."""
        latest_status_subquery = (
            StatusChange.objects.filter(study_id=OuterRef("id"))
            .order_by("-pk")
            .values("status")[:1]
        )

        return queryset.annotate(latest_status=Subquery(latest_status_subquery)).filter(
            latest_status__in=value
        )

    def filter_faculties(self, queryset, name, value):
        return self.filter_select_options(queryset, name, value)

    def filter_select_options(self, queryset, name, value):
        """
        A generic method for creating filters based on SelectQuestion.
        For this to work:
            - the SelectQuestion needs to have a string_id, so that it gets
            annotated to the Study
            - You'll need to use a ModelMultipleChoiceFilter, with:
                - the SelectOptions as the queryset
                - the annotation_key as the name
        Then you can make a method for this filter which calls this method
        """
        if not value:
            return queryset

        # We'll receive a list of SelectOption instances, but  we'll just need
        # ids
        option_ids = [option.id for option in value]

        queries = Q()
        for option_id in option_ids:
            filter = {f"{name}__contains": option_id}
            queries |= Q(**filter)

        return queryset.filter(queries)


class StudyType(GQLListObjectType):
    title = String()
    latest_submission_id = ID(required=True)
    status = Field((GQLSubmissionStatus), required=True)
    actions = List(NonNull(ActionEnum), required=True)
    status = Field(GQLSubmissionStatus, required=True)
    updated_at = DateTime(required=True)

    class Meta:
        model = Study
        fields = [
            "id",
            "created_by",
            "created_at",
            "reference",
            "title",
        ]
        filterset_class = StudyFilter
        search_fields = [
            "reference",
            "created_by__first_name",
            "created_by__last_name",
            "title",
        ]

    @classmethod
    def get_queryset(
        cls,
        queryset: QuerySet[Study],
        info: ResolveInfo,
    ) -> QuerySet[Study]:
        return queryset

    @staticmethod
    def resolve_latest_submission_id(parent: Study, info: ResolveInfo) -> int:
        return UserFormSubmission.objects.filter(study=parent).last().pk

    @staticmethod
    def resolve_status(parent: Study, info: ResolveInfo) -> SubmissionStatus:
        return parent.status

    @staticmethod
    def resolve_actions(parent: Study, info: ResolveInfo) -> list[ActionEnum]:
        user = info.context.user
        study_actions = StudyActions(parent, user)
        return study_actions.get_available_actions()

    @staticmethod
    def resolve_updated_at(parent: Study, info: ResolveInfo) -> datetime:
        return parent.updated_at
