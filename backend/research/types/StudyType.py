from django_filters import FilterSet, ModelMultipleChoiceFilter
from graphene import ID, List, NonNull, ResolveInfo, String

from django.db.models import QuerySet

from api.gql_list_object_type import GQLListObjectType
from research.utils.study_actions import ActionEnum
from form.models import UserFormSubmission
from main.models import User
from research.models.study import Study
from research.utils.study_actions import StudyActions


class StudyFilter(FilterSet):

    created_by_ids = ModelMultipleChoiceFilter(
        field_name="created_by_id", queryset=User.objects.all()
    )


class StudyType(GQLListObjectType):
    title = String(required=True)
    latest_submission_id = ID(required=True)
    actions = List(NonNull(ActionEnum), required=True)

    class Meta:
        model = Study
        fields = [
            "id",
            "created_by",
            "reference",
        ]
        filterset_class = StudyFilter
        search_fields = ["title", "reference"]

    @classmethod
    def get_queryset(
        cls,
        queryset: QuerySet[Study],
        info: ResolveInfo,
    ) -> QuerySet[Study]:
        return queryset

    @staticmethod
    def resolve_title(parent: Study, info: ResolveInfo) -> str:
        return parent.name

    @staticmethod
    def resolve_latest_submission_id(parent: Study, info: ResolveInfo) -> int:
        return UserFormSubmission.objects.filter(study=parent).last().pk

    @staticmethod
    def resolve_actions(parent: Study, info: ResolveInfo) -> list[ActionEnum]:
        user = info.context.user
        study_actions = StudyActions(parent, user)
        return study_actions.get_available_actions()
