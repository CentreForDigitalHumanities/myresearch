from typing import Optional
from graphene import Field, List, ObjectType, ResolveInfo, ID, String, NonNull

from django.db.models import QuerySet

from study.models import Study
from study.types.StudyType import StudyType
from main.models import MRPermission


class StudyQuery(ObjectType):
    study = Field(
        StudyType,
        id=ID(required=True),
        mrpermission=String(required=True),
    )

    studies = List(
        NonNull(
            StudyType,
        ),
        mrpermission=String(required=True),
        required=True,
    )

    @staticmethod
    def resolve_study(
        root, info: ResolveInfo, id: int, mrpermission: str
    ) -> Optional[Study]:
        queryset = StudyType.get_queryset(
            Study.objects,
            info,
            mrpermission=mrpermission,
        )
        try:
            return queryset.get(id=id)
        except Study.DoesNotExist:
            return None

    @staticmethod
    def resolve_studies(root, info: ResolveInfo, mrpermission: str) -> QuerySet[Study]:
        return StudyType.get_queryset(
            Study.objects, info, mrpermission=mrpermission
        ).all()
