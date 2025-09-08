from graphene import ID, Boolean, Interface, ResolveInfo, String, Union
from graphene_django import DjangoObjectType

from django.db.models import QuerySet

from form.types.SelectOptionType import SelectOptionType
from form.models import (
    SelectOption,
    TrueFalseQuestion,
    DateQuestion,
    FileUploadQuestion,
    NumberQuestion,
    SelectQuestion,
    TextQuestion,
)


class BaseQuestionInterface(Interface):
    """
    Based on the BaseQuestion model, which is the base class for all question 
    models. Types implementing this interface should be based on models that 
    extend BaseQuestion.
    """

    id = ID(required=True)
    text_nl = String(required=True)
    text_en = String(required=True)
    description_nl = String(required=True)
    description_en = String(required=True)
    required = Boolean(required=True)


class DateQuestionType(DjangoObjectType):
    class Meta:
        model = DateQuestion
        interfaces = [BaseQuestionInterface]
        fields = [
            "future_only",
        ]

    @classmethod
    def get_queryset(
        cls, queryset: QuerySet[DateQuestion], info: ResolveInfo
    ) -> QuerySet[DateQuestion]:
        return queryset


class FileUploadQuestionType(DjangoObjectType):
    class Meta:
        model = FileUploadQuestion
        interfaces = [BaseQuestionInterface]
        fields = [
            "size_limit",
        ]

    @classmethod
    def get_queryset(
        cls, queryset: QuerySet[FileUploadQuestion], info: ResolveInfo
    ) -> QuerySet[FileUploadQuestion]:
        return queryset


class NumberQuestionType(DjangoObjectType):
    class Meta:
        model = NumberQuestion
        interfaces = [BaseQuestionInterface]
        fields = [
            "positive_only",
        ]

    @classmethod
    def get_queryset(
        cls, queryset: QuerySet[NumberQuestion], info: ResolveInfo
    ) -> QuerySet[NumberQuestion]:
        return queryset


class SelectQuestionType(DjangoObjectType):
    class Meta:
        model = SelectQuestion
        interfaces = [BaseQuestionInterface]
        fields = [
            "options",
            "multiple",
        ]

    @classmethod
    def get_queryset(
        cls, queryset: QuerySet[SelectQuestion], info: ResolveInfo
    ) -> QuerySet[SelectQuestion]:
        return queryset

    @staticmethod
    def resolve_options(parent: SelectQuestion, info: ResolveInfo):
        return SelectOptionType.get_queryset(SelectOption.objects, info).filter(
            question=parent
        )


class TextQuestionType(DjangoObjectType):
    class Meta:
        model = TextQuestion
        interfaces = [BaseQuestionInterface]
        fields = [
            "placeholder_nl",
            "placeholder_en",
            "lines",
        ]

    @classmethod
    def get_queryset(
        cls, queryset: QuerySet[TextQuestion], info: ResolveInfo
    ) -> QuerySet[TextQuestion]:
        return queryset


class TrueFalseQuestionType(DjangoObjectType):
    class Meta:
        model = TrueFalseQuestion
        interfaces = [BaseQuestionInterface]
        fields = [
            "default_value",
        ]

    @classmethod
    def get_queryset(
        cls, queryset: QuerySet[TrueFalseQuestion], info: ResolveInfo
    ) -> QuerySet[TrueFalseQuestion]:
        return queryset


# Union Type
class QuestionType(Union):
    class Meta:
        interfaces = [BaseQuestionInterface]
        types = (
            TrueFalseQuestionType,
            DateQuestionType,
            FileUploadQuestionType,
            NumberQuestionType,
            SelectQuestionType,
            TextQuestionType,
        )

    @classmethod
    def resolve_type(cls, instance, info: ResolveInfo):
        if isinstance(instance, TrueFalseQuestion):
            return TrueFalseQuestionType
        elif isinstance(instance, DateQuestion):
            return DateQuestionType
        elif isinstance(instance, FileUploadQuestion):
            return FileUploadQuestionType
        elif isinstance(instance, NumberQuestion):
            return NumberQuestionType
        elif isinstance(instance, SelectQuestion):
            return SelectQuestionType
        elif isinstance(instance, TextQuestion):
            return TextQuestionType
        return None
