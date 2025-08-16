from graphene import ResolveInfo
from graphene_django import DjangoObjectType

from django.db.models import QuerySet

from form.models import StepInfoQuestion


class StepInfoQuestionType(DjangoObjectType):
    class Meta:
        model = StepInfoQuestion
        fields = [
            "id",
            "step_info",
            "text_nl",
            "text_en",
            "link"
        ]

    @classmethod
    def get_queryset(
        cls, queryset: QuerySet[StepInfoQuestion], info: ResolveInfo
    ) -> QuerySet[StepInfoQuestion]:
        return queryset
