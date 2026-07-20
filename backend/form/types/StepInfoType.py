from graphene import ResolveInfo
from graphene_django import DjangoObjectType

from django.db.models import QuerySet

from form.models import StepInfo


class StepInfoType(DjangoObjectType):
    class Meta:
        model = StepInfo
        fields = [
            "id",
            "text_nl",
            "text_en",
            "content_nl",
            "content_en",
        ]

    @classmethod
    def get_queryset(
        cls, queryset: QuerySet[StepInfo], info: ResolveInfo
    ) -> QuerySet[StepInfo]:
        return queryset