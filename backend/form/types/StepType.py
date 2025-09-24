from graphene import List, NonNull, ResolveInfo
from graphene_django import DjangoObjectType

from django.db.models import QuerySet, Model

from form.models import (
    DateQuestion,
    Step,
    StepInfoQuestion,
    StepInfoText,
    BaseQuestion,
    DateQuestion,
    FileUploadQuestion,
    StepInfoText,
    StepInfoQuestion,
    MRForm,
    NumberQuestion,
    SelectQuestion,
    TextQuestion,
    TrueFalseQuestion,
)
from form.types.QuestionType import BaseQuestionInterface
from form.types.StepInfoTextType import StepInfoTextType
from form.types.StepInfoQuestionType import StepInfoQuestionType
from form.types.QuestionType import (
    BaseQuestionInterface,
    DateQuestionType,
    FileUploadQuestionType,
    NumberQuestionType,
    SelectQuestionType,
    TextQuestionType,
    TrueFalseQuestionType,
)


class StepType(DjangoObjectType):
    questions = List(NonNull(BaseQuestionInterface), required=True)

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
            "parent",
            "substeps",
            "info_questions",
            "info_texts",
            "questions",
        ]

    @classmethod
    def get_queryset(
        cls, queryset: QuerySet[Step], info: ResolveInfo
    ) -> QuerySet[Step]:
        return queryset

    @staticmethod
    def resolve_info_texts(parent: Step, info: ResolveInfo) -> QuerySet[StepInfoText]:
        return StepInfoTextType.get_queryset(StepInfoText.objects, info).filter(
            step=parent
        )

    @staticmethod
    def resolve_info_questions(
        parent: Step, info: ResolveInfo
    ) -> QuerySet[StepInfoQuestion]:
        return StepInfoQuestionType.get_queryset(StepInfoQuestion.objects, info).filter(
            step=parent
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
