from django_filters import FilterSet, ModelMultipleChoiceFilter
from graphene import ID, ResolveInfo, String

from django.db.models import QuerySet

from api.gql_list_object_type import GQLListObjectType
from form.models import UserFormSubmission
from main.models import User
from research.models import Study


class StudyFilter(FilterSet):

    created_by_ids = ModelMultipleChoiceFilter(
        field_name="created_by_id", queryset=User.objects.all()
    )


class StudyType(GQLListObjectType):
    title = String(required=True)
    latest_submission_id = ID(required=True)

    class Meta:
        model = Study
        fields = [
            "id",
            "created_by",
        ]
        filterset_class = StudyFilter
        search_fields = ["title"]

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
