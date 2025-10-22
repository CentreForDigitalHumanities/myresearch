from graphene import ResolveInfo
from graphene_django import DjangoObjectType

from django.db.models import QuerySet

from study.models import Study
from main.models import User, MRPermission


class StudyType(DjangoObjectType):
    class Meta:
        model = Study
        fields = [
            "id",
            "title",
            "created_by",
        ]

    @classmethod
    def get_queryset(
        cls,
        queryset: QuerySet[Study],
        info: ResolveInfo,
        mrpermission: str,
    ) -> QuerySet[Study]:
        """
        Return the queryset of studies, based on the permission, defined in the
        query.
        """

        user = info.context.user

        return queryset.accessible_objects(user, mrpermission)
