from typing import Optional
from graphene import Field, List, ObjectType, ResolveInfo, Int

from django.db.models import QuerySet

from study.models import Study
from study.types.StudyType import StudyType
from main.models import MRPermissionTypes


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
        id=Int(),
    )

    my_study_list = List(
        StudyType,
    )

    def resolve_study(root, info: ResolveInfo, id) -> Optional[Study]:
        try:
            study = Study.objects.get(id=id)
        except Study.DoesNotExist:
            return None
        if study.can_be_accessed_by(info.context.user, MRPermissionTypes.VIEW):
            return study
        return None

    def resolve_study_list(
        root,
        info: ResolveInfo,
    ) -> QuerySet[Study]:
        queryset = StudyType.get_queryset(
            Study.objects, info, permission=MRPermissionTypes.VIEW
        )
        return queryset.all()

    def resolve_my_study(root, info: ResolveInfo, id) -> Optional[Study]:
        try:
            study = Study.objects.get(id=id)
        except Study.DoesNotExist:
            return None
        if study.can_be_accessed_by(info.context.user, MRPermissionTypes.EDIT):
            return study
        return None

    def resolve_my_study_list(
        root,
        info: ResolveInfo,
    ) -> QuerySet[Study]:
        queryset = StudyType.get_queryset(
            Study.objects, info, permission=MRPermissionTypes.EDIT
        )
        return queryset.all()
