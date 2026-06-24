from graphene import (
    ID,
    Int,
    Boolean,
    Interface,
    ResolveInfo,
    String,
    Union,
    ObjectType,
    List,
    NonNull,
    JSONString,
)

from form.models import (
    BaseQuestion,
    TrueFalseQuestion,
    DateQuestion,
    FileUploadQuestion,
    NumberQuestion,
    SelectQuestion,
    TextQuestion,
)
from form.types.SelectOptionType import SelectOptionType


class BaseQuestionInterface(Interface):
    """
    Base interface for user questions, containing fields common to all question types.
    """

    question_id = ID(
        required=True, description="The ID of the question this is based on."
    )
    repeat_index = Int(required=False)
    answer = JSONString()
    response_id = ID()

    text_nl = String(required=True)
    text_en = String(required=True)
    description_nl = String(required=True)
    description_en = String(required=True)
    required = Boolean(required=True)
    has_conditions = Boolean(required=True)
    background = Boolean()

    @classmethod
    def resolve_type(cls, instance, info):
        """Resolve to the correct concrete type based on the question type."""
        if hasattr(instance, "question"):
            question = instance.question
        else:
            # Questions created by UserFormResolver._create_question_instance
            # should always have the question object; this is a fallback.
            # TODO: Implement a logger to warn us of such cases in production.
            question = BaseQuestion.objects.get(pk=instance.question_id)

        if hasattr(question, "textquestion"):
            return TextQuestionType
        elif hasattr(question, "numberquestion"):
            return NumberQuestionType
        elif hasattr(question, "truefalsequestion"):
            return TrueFalseQuestionType
        elif hasattr(question, "datequestion"):
            return DateQuestionType
        elif hasattr(question, "selectquestion"):
            return SelectQuestionType
        elif hasattr(question, "fileuploadquestion"):
            return FileUploadQuestionType

        # Should never happen - default fallback
        return TextQuestionType


class BaseQuestionMixin:
    """Mixin providing common resolvers for all question types."""

    @staticmethod
    def resolve_text_nl(parent, info: ResolveInfo):
        return parent.question.text_nl

    @staticmethod
    def resolve_has_conditions(parent, info: ResolveInfo):
        return parent.question.has_conditions

    @staticmethod
    def resolve_text_en(parent, info: ResolveInfo):
        return parent.question.text_en

    @staticmethod
    def resolve_description_nl(parent, info: ResolveInfo):
        return parent.question.description_nl

    @staticmethod
    def resolve_description_en(parent, info: ResolveInfo):
        return parent.question.description_en

    @staticmethod
    def resolve_required(parent, info: ResolveInfo):
        return parent.question.required


class TextQuestionType(BaseQuestionMixin, ObjectType):
    class Meta:
        interfaces = [BaseQuestionInterface]

    placeholder_nl = String()
    placeholder_en = String()
    lines = Int(required=True)

    def __init__(self, question=None, **kwargs):
        super().__init__(**kwargs)
        self.question = question

    @staticmethod
    def resolve_placeholder_nl(parent, info: ResolveInfo):
        if hasattr(parent.question, "textquestion"):
            return parent.question.textquestion.placeholder_nl
        return parent.question.placeholder_nl

    @staticmethod
    def resolve_placeholder_en(parent, info: ResolveInfo):
        if hasattr(parent.question, "textquestion"):
            return parent.question.textquestion.placeholder_en
        return parent.question.placeholder_en

    @staticmethod
    def resolve_lines(parent, info: ResolveInfo):
        if hasattr(parent.question, "textquestion"):
            return parent.question.textquestion.lines
        return parent.question.lines


class NumberQuestionType(BaseQuestionMixin, ObjectType):
    class Meta:
        interfaces = [BaseQuestionInterface]

    positive_only = Boolean(required=True)

    def __init__(self, question=None, **kwargs):
        super().__init__(**kwargs)
        self.question = question

    @staticmethod
    def resolve_positive_only(parent, info: ResolveInfo):
        if hasattr(parent.question, "numberquestion"):
            return parent.question.numberquestion.positive_only
        return parent.question.positive_only


class TrueFalseQuestionType(BaseQuestionMixin, ObjectType):
    class Meta:
        interfaces = [BaseQuestionInterface]

    default_value = Boolean(required=True)

    def __init__(self, question=None, **kwargs):
        super().__init__(**kwargs)
        self.question = question

    @staticmethod
    def resolve_default_value(parent, info: ResolveInfo):
        # Ensure we have the TrueFalseQuestion subclass
        if hasattr(parent.question, "truefalsequestion"):
            return parent.question.truefalsequestion.default_value
        return parent.question.default_value


class DateQuestionType(BaseQuestionMixin, ObjectType):
    class Meta:
        interfaces = [BaseQuestionInterface]

    future_only = Boolean(required=True)

    def __init__(self, question=None, **kwargs):
        super().__init__(**kwargs)
        self.question = question

    @staticmethod
    def resolve_future_only(parent, info: ResolveInfo):
        if hasattr(parent.question, "datequestion"):
            return parent.question.datequestion.future_only
        return parent.question.future_only


class SelectQuestionType(BaseQuestionMixin, ObjectType):
    class Meta:
        interfaces = [BaseQuestionInterface]

    multiple = Boolean(required=True)
    options = List(NonNull(SelectOptionType), required=True)

    def __init__(self, question=None, **kwargs):
        super().__init__(**kwargs)
        self.question = question

    @staticmethod
    def resolve_multiple(parent, info: ResolveInfo):
        if hasattr(parent.question, "selectquestion"):
            return parent.question.selectquestion.multiple
        return parent.question.multiple

    @staticmethod
    def resolve_options(parent, info: ResolveInfo):
        if hasattr(parent.question, "selectquestion"):
            return parent.question.selectquestion.options.all()
        return parent.question.options.all()


class FileUploadQuestionType(BaseQuestionMixin, ObjectType):
    class Meta:
        interfaces = [BaseQuestionInterface]

    size_limit = Int(required=True)

    def __init__(self, question=None, **kwargs):
        super().__init__(**kwargs)
        self.question = question

    @staticmethod
    def resolve_size_limit(parent, info: ResolveInfo):
        if hasattr(parent.question, "fileuploadquestion"):
            return parent.question.fileuploadquestion.size_limit
        return parent.question.size_limit


# Union Type
class QuestionType(Union):
    class Meta:
        types = (
            TextQuestionType,
            NumberQuestionType,
            TrueFalseQuestionType,
            DateQuestionType,
            SelectQuestionType,
            FileUploadQuestionType,
        )

    @classmethod
    def resolve_type(cls, instance, info: ResolveInfo):
        # Get the actual question to determine type
        question = getattr(instance, "question", None)
        if question is None:
            question = BaseQuestion.objects.get(pk=instance.question_id)

        if isinstance(question, TextQuestion):
            return TextQuestionType
        elif isinstance(question, NumberQuestion):
            return NumberQuestionType
        elif isinstance(question, TrueFalseQuestion):
            return TrueFalseQuestionType
        elif isinstance(question, DateQuestion):
            return DateQuestionType
        elif isinstance(question, SelectQuestion):
            return SelectQuestionType
        elif isinstance(question, FileUploadQuestion):
            return FileUploadQuestionType
        return None
