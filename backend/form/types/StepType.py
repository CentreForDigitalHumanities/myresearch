from graphene import NonNull, ResolveInfo, List, Field
from graphene_django import DjangoObjectType

from django.db.models import QuerySet, Model

from form.types.QuestionType import (
    BaseQuestionInterface,
    DateQuestionType,
    FileUploadQuestionType,
    NumberQuestionType,
    SelectQuestionType,
    TextQuestionType,
    TrueFalseQuestionType,
)
from form.types.StepInfoType import StepInfoType
from form.models import (
    BaseQuestion,
    BaseQuestion,
    DateQuestion,
    FileUploadQuestion,
    NumberQuestion,
    SelectQuestion,
    Step,
    StepInfo,
    TextQuestion,
    TrueFalseQuestion,
)


class StepType(DjangoObjectType):
    questions = List(NonNull(BaseQuestionInterface))
    info = Field(StepInfoType)

    class Meta:
        model = Step
        fields = [
            "id",
            "name_nl",
            "name_en",
            "description_nl",
            "description_en",
            "slug",
            "form",
            "form_order",
            "parent",
            "parent_order",
            "substeps",
            "info",
        ]

    @classmethod
    def get_queryset(
        cls, queryset: QuerySet[Step], info: ResolveInfo
    ) -> QuerySet[Step]:
        return queryset

    @staticmethod
    def resolve_substeps(parent: Step, info: ResolveInfo) -> QuerySet[Step]:
        return (
            StepType.get_queryset(Step.objects, info)
            .filter(parent=parent)
            .order_by("parent_order")
        )

    @staticmethod
    def resolve_questions(parent: Step, info: ResolveInfo) -> list[BaseQuestion]:
        question_types: list[tuple[type[DjangoObjectType], type[Model]]] = [
            (TrueFalseQuestionType, TrueFalseQuestion),
            (DateQuestionType, DateQuestion),
            (FileUploadQuestionType, FileUploadQuestion),
            (NumberQuestionType, NumberQuestion),
            (SelectQuestionType, SelectQuestion),
            (TextQuestionType, TextQuestion),
        ]

        questions: list[BaseQuestion] = []
        for question_type, question_model in question_types:
            question_queryset = question_type.get_queryset(
                question_model.objects, info
            ).filter(step=parent)
            questions.extend(question_queryset)

        return questions

    @staticmethod
    def resolve_info(parent: Step, info: ResolveInfo) -> StepInfo | None:
        try:
            return StepInfoType.get_queryset(StepInfo.objects, info).get(step=parent)
        except StepInfo.DoesNotExist:
            return None
