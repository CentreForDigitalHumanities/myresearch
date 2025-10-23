from graphene import ResolveInfo
from graphene_django import DjangoObjectType

from django.db.models import QuerySet

from study.models import Study


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
    ) -> QuerySet[Study]:
        return queryset
