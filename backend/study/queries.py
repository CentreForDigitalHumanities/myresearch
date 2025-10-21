from typing import Optional
from graphene import Field, List, ObjectType, ResolveInfo, Int, ID

from django.db.models import QuerySet

from study.models import Study
from study.types.StudyType import StudyType
from main.models import MRPermission


class StudyQuery(ObjectType):
    study = Field(
        StudyType,
        id=ID(required=True),
    )

    study_list = List(
        StudyType,
    )

    my_study = Field(
        StudyType,
        id=ID(required=True),
    )

    my_study_list = List(
        StudyType,
    )

    @staticmethod
    def resolve_study(root, info: ResolveInfo, id: int) -> Optional[Study]:
        queryset = StudyType.get_queryset(Study.objects, info, permission=MRPermission.VIEW)
        try:
            return queryset.get(id=id)
        except Study.DoesNotExist:
            return None

    @staticmethod
    def resolve_study_list(
        root,
        info: ResolveInfo,
    ) -> QuerySet[Study]:
        queryset = StudyType.get_queryset(
            Study.objects, info, permission=MRPermission.VIEW
        )
        return queryset.all()

    @staticmethod
    def resolve_my_study(root, info: ResolveInfo, id: int) -> Optional[Study]:
        try:
            study = Study.objects.get(id=id)
        except Study.DoesNotExist:
            return None
        if study.can_be_accessed_by(info.context.user, MRPermission.EDIT):
            return study
        return None

    @staticmethod
    def resolve_my_study_list(
        root,
        info: ResolveInfo,
    ) -> QuerySet[Study]:
        queryset = StudyType.get_queryset(
            Study.objects, info, permission=MRPermission.EDIT
        )
        return queryset.all()
