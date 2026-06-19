from typing import Optional
from graphene import Field, List, ObjectType, ResolveInfo, ID, String, NonNull
from django.db.models import QuerySet
from api.graphql.pagination_field import GQLListPaginationConnectionField
from research.models.reviews import StatusChange
from research.models.study import Study
from research.types.StudyType import StudyType
from research.types.StatusChangeType import StatusChangeType


class StudyQuery(ObjectType):
    study = Field(
        StudyType,
        id=ID(required=True),
        mr_permission=String(required=True),
    )

    studies = List(
        NonNull(
            StudyType,
        ),
        mr_permission=String(required=True),
        required=True,
    )

    study_pages = GQLListPaginationConnectionField(
        StudyType,
        mr_permission=String(required=True),
    )

    status_changes = List(
        NonNull(
            StatusChangeType,
        ),
        mr_permission=String(required=True),
        study_id=ID(required=False),
        required=True,
    )

    @staticmethod
    def resolve_study(
        root, info: ResolveInfo, id: int, mr_permission: str
    ) -> Optional[Study]:
        queryset = StudyType.get_queryset(
            Study.objects,
            info,
        ).accessible_objects(info.context.user, mr_permission)
        try:
            return queryset.get(id=id)
        except Study.DoesNotExist:
            return None

    @staticmethod
    def resolve_studies(root, info: ResolveInfo, mr_permission: str) -> QuerySet[Study]:
        return StudyType.get_queryset(Study.objects, info).accessible_objects(
            info.context.user, mr_permission
        )

    @staticmethod
    def resolve_study_pages(
        root, info: ResolveInfo, mr_permission: str, **kwargs
    ) -> QuerySet[Study]:
        return StudyType.get_queryset(Study.objects, info).accessible_objects(
            info.context.user, mr_permission
        )

    @staticmethod
    def resolve_status_changes(
        root, info: ResolveInfo, mr_permission: str, study_id: str
    ) -> QuerySet[StatusChange]:
        queryset = StatusChangeType.get_queryset(StatusChange.objects, info)
        queryset = queryset.accessible_objects(info.context.user, mr_permission)
        if study_id:
            study = Study.objects.get(pk=study_id)
            queryset = queryset.filter(study=study)
        return queryset
