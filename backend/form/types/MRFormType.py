from graphene import List, NonNull, ResolveInfo
from graphene_django import DjangoObjectType

from django.db.models import QuerySet, Model

from form.models import (
    BaseQuestion,
    DateQuestion,
    FileUploadQuestion,
    FormInfoText,
    FormInfoQuestion,
    MRForm,
    NumberQuestion,
    SelectQuestion,
    TextQuestion,
    TrueFalseQuestion,
)
from form.types.QuestionType import (
    BaseQuestionInterface,
    DateQuestionType,
    FileUploadQuestionType,
    NumberQuestionType,
    SelectQuestionType,
    TextQuestionType,
    TrueFalseQuestionType,
)
from form.types.FormInfoTextType import FormInfoTextType
from form.types.FormInfoQuestionType import FormInfoQuestionType


class MRFormType(DjangoObjectType):
    questions = List(NonNull(BaseQuestionInterface), required=True)

    class Meta:
        model = MRForm
        fields = [
            "id",
            "name_nl",
            "name_en",
            "description_nl",
            "description_en",
            "slug",
            "version",
            "created_at",
            "updated_at",
            "parent",
            "subforms",
            "info_questions",
            "info_texts",
            "questions",
        ]

    @classmethod
    def get_queryset(
        cls, queryset: QuerySet[MRForm], info: ResolveInfo
    ) -> QuerySet[MRForm]:
        return queryset

    @staticmethod
    def resolve_info_texts(parent: MRForm, info: ResolveInfo) -> QuerySet[FormInfoText]:
        return FormInfoTextType.get_queryset(FormInfoText.objects, info).filter(
            form=parent
        )

    @staticmethod
    def resolve_info_questions(
        parent: MRForm, info: ResolveInfo
    ) -> QuerySet[FormInfoQuestion]:
        return FormInfoQuestionType.get_queryset(FormInfoQuestion.objects, info).filter(
            form=parent
        )

    @staticmethod
    def resolve_questions(parent: MRForm, info: ResolveInfo) -> list[BaseQuestion]:
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
            ).filter(form=parent)
            questions.extend(question_queryset)

        return questions
