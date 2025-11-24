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
    SelectOption,
    TrueFalseQuestion,
    DateQuestion,
    FileUploadQuestion,
    NumberQuestion,
    SelectQuestion,
    TextQuestion,
)
from form.types.SelectOptionType import SelectOptionType


class BaseUserQuestionInterface(Interface):
    """
    Base interface for user questions, containing fields common to all question types.
    """

    question_id = ID(
        required=True, description="The ID of the question this is based on."
    )
    repeat_index = Int(required=True)
    answer = JSONString()

    id = ID(required=True)
    text_nl = String(required=True)
    text_en = String(required=True)
    description_nl = String(required=True)
    description_en = String(required=True)
    required = Boolean(required=True)

    @classmethod
    def resolve_type(cls, instance, info):
        """Resolve to the correct concrete type based on the question type."""
        # The instance should have a question attribute
        if hasattr(instance, "question"):
            question = instance.question
        else:
            # Fallback: fetch the question from the database
            question = BaseQuestion.objects.get(pk=instance.question_id)

        # Use hasattr to check for Django's reverse relation attributes
        if hasattr(question, "textquestion"):
            return UserTextQuestionType
        elif hasattr(question, "numberquestion"):
            return UserNumberQuestionType
        elif hasattr(question, "truefalsequestion"):
            return UserTrueFalseQuestionType
        elif hasattr(question, "datequestion"):
            return UserDateQuestionType
        elif hasattr(question, "selectquestion"):
            return UserSelectQuestionType
        elif hasattr(question, "fileuploadquestion"):
            return UserFileUploadQuestionType

        # Should never happen - default fallback
        return UserTextQuestionType


class BaseUserQuestionMixin:
    """Mixin providing common resolvers for all user question types."""

    @staticmethod
    def resolve_id(parent, info: ResolveInfo):
        return parent.question_id

    @staticmethod
    def resolve_text_nl(parent, info: ResolveInfo):
        return parent.question.text_nl

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


class UserTextQuestionType(BaseUserQuestionMixin, ObjectType):
    class Meta:
        interfaces = [BaseUserQuestionInterface]

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


class UserNumberQuestionType(BaseUserQuestionMixin, ObjectType):
    class Meta:
        interfaces = [BaseUserQuestionInterface]

    positive_only = Boolean(required=True)

    def __init__(self, question=None, **kwargs):
        super().__init__(**kwargs)
        self.question = question

    @staticmethod
    def resolve_positive_only(parent, info: ResolveInfo):
        if hasattr(parent.question, "numberquestion"):
            return parent.question.numberquestion.positive_only
        return parent.question.positive_only


class UserTrueFalseQuestionType(BaseUserQuestionMixin, ObjectType):
    class Meta:
        interfaces = [BaseUserQuestionInterface]

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


class UserDateQuestionType(BaseUserQuestionMixin, ObjectType):
    class Meta:
        interfaces = [BaseUserQuestionInterface]

    future_only = Boolean(required=True)

    def __init__(self, question=None, **kwargs):
        super().__init__(**kwargs)
        self.question = question

    @staticmethod
    def resolve_future_only(parent, info: ResolveInfo):
        if hasattr(parent.question, "datequestion"):
            return parent.question.datequestion.future_only
        return parent.question.future_only


class UserSelectQuestionType(BaseUserQuestionMixin, ObjectType):
    class Meta:
        interfaces = [BaseUserQuestionInterface]

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


class UserFileUploadQuestionType(BaseUserQuestionMixin, ObjectType):
    class Meta:
        interfaces = [BaseUserQuestionInterface]

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
class UserQuestionType(Union):
    class Meta:
        types = (
            UserTextQuestionType,
            UserNumberQuestionType,
            UserTrueFalseQuestionType,
            UserDateQuestionType,
            UserSelectQuestionType,
            UserFileUploadQuestionType,
        )

    @classmethod
    def resolve_type(cls, instance, info: ResolveInfo):
        # Get the actual question to determine type
        question = BaseQuestion.objects.get(pk=instance.question_id)

        if isinstance(question, TextQuestion):
            return UserTextQuestionType
        elif isinstance(question, NumberQuestion):
            return UserNumberQuestionType
        elif isinstance(question, TrueFalseQuestion):
            return UserTrueFalseQuestionType
        elif isinstance(question, DateQuestion):
            return UserDateQuestionType
        elif isinstance(question, SelectQuestion):
            return UserSelectQuestionType
        elif isinstance(question, FileUploadQuestion):
            return UserFileUploadQuestionType
        return None
