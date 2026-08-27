from graphene import ResolveInfo
from graphene_django import DjangoObjectType

from django.db.models import QuerySet

from form.models import StepInfoText


class StepInfoTextType(DjangoObjectType):
    class Meta:
        model = StepInfoText
        fields = [
            "id",
            "text_nl",
            "text_en",
            "content_nl",
            "content_en",
        ]

    @classmethod
    def get_queryset(
        cls, queryset: QuerySet[StepInfoText], info: ResolveInfo
    ) -> QuerySet[StepInfoText]:
        return queryset
