from graphene import ResolveInfo
from graphene_django import DjangoObjectType

from django.db.models import QuerySet

from form.types.StepInfoTextType import StepInfoTextType
from form.types.StepInfoQuestionType import StepInfoQuestionType
from form.models import StepInfo, StepInfoQuestion, StepInfoText


class StepInfoType(DjangoObjectType):
    class Meta:
        model = StepInfo
        fields = [
            "id",
            "step",
            "texts",
            "questions",
        ]

    @classmethod
    def get_queryset(
        cls, queryset: QuerySet[StepInfo], info: ResolveInfo
    ) -> QuerySet[StepInfo]:
        return queryset

    @staticmethod
    def resolve_texts(parent: StepInfo, info: ResolveInfo) -> QuerySet[StepInfoText]:
        return StepInfoTextType.get_queryset(StepInfoText.objects, info).filter(
            step_info=parent
        )

    @staticmethod
    def resolve_questions(
        parent: StepInfo, info: ResolveInfo
    ) -> QuerySet[StepInfoQuestion]:
        return StepInfoQuestionType.get_queryset(StepInfoQuestion.objects, info).filter(
            step_info=parent
        )
