from django.db.models import QuerySet

from api.gql_list_object_type import GQLListObjectType
from research.models.reviews import StatusChange, SubmissionStatus
from research.models.study import Study
from research.types.StudyType import StudyType
from graphene import ID, Enum, List, NonNull, ResolveInfo, String, Field


class StatusChangeType(GQLListObjectType):
    status = Field(Enum.from_enum(SubmissionStatus), required=True)
    study = Field(StudyType, required=True)

    class Meta:
        model = StatusChange
        fields = [
            "id",
            "created_at",
        ]

    @classmethod
    def get_queryset(
        cls,
        queryset: QuerySet[StatusChange],
        info: ResolveInfo,
    ) -> QuerySet[StatusChange]:
        return queryset

    @staticmethod
    def resolve_status(parent: StatusChange, info: ResolveInfo) -> SubmissionStatus:
        return parent.status

    @staticmethod
    def resolve_study(parent: StatusChange, info: ResolveInfo) -> Study:
        return parent.study
