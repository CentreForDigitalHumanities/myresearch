from graphene import ResolveInfo
from graphene_django import DjangoObjectType

from django.db.models import QuerySet

from form.models import MRFormConfig


class MRFormConfigType(DjangoObjectType):

    class Meta:
        model = MRFormConfig
        fields = [
            "id",
            "name",
            "version",
            "created_at",
            "updated_at",
            "form",
        ]

    @classmethod
    def get_queryset(
        cls, queryset: QuerySet[MRFormConfig], info: ResolveInfo
    ) -> QuerySet[MRFormConfig]:
        return queryset
