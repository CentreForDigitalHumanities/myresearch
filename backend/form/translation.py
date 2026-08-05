from modeltranslation.translator import register, TranslationOptions

from .models import (
    BaseQuestion,
    DateQuestion,
    FileUploadQuestion,
    StepInfoText,
    MRForm,
    Step,
    NumberQuestion,
    SelectOption,
    TextQuestion,
    RepeatableTextQuestion,
    SelectQuestion,
    TrueFalseQuestion,
    RepeatableStep,
)


@register(MRForm)
class MRFormTranslationOptions(TranslationOptions):
    fields = ["name"]


@register(Step)
class StepTranslationOptions(TranslationOptions):
    fields = ["name", "description"]


@register(RepeatableStep)
class RepeatableStepTranslationOptions(TranslationOptions):
    """
    RepeatableStep inherits the translatable fields from StepTranslationOptions,
    but must still be registered regardless.
    """

    fields = []


@register(StepInfoText)
class FormInfoTextTranslationOptions(TranslationOptions):
    fields = ["text"]


@register(BaseQuestion)
class BaseQuestionTranslationOptions(TranslationOptions):
    fields = ["text", "description"]


@register(SelectOption)
class SelectOptionTranslationOptions(TranslationOptions):
    fields = ["label"]


@register(SelectQuestion)
class SelectQuestionTranslationOptions(TranslationOptions):
    pass


@register(TrueFalseQuestion)
class TrueFalseQuestionTranslationOptions(TranslationOptions):
    pass


@register(TextQuestion)
class TextQuestionTranslationOptions(TranslationOptions):
    fields = ["placeholder"]


@register(RepeatableTextQuestion)
class RepeatableTextQuestionTranslationOptions(TranslationOptions):
    """
    RepeatableTextQuestion inherits the translatable fields from TextQuestionTranslationOptions,
    but must still be registered regardless.
    """

    fields = []


@register(NumberQuestion)
class NumberQuestionTranslationOptions(TranslationOptions):
    pass


@register(DateQuestion)
class DateQuestionTranslationOptions(TranslationOptions):
    pass


@register(FileUploadQuestion)
class FileUploadQuestionTranslationOptions(TranslationOptions):
    pass
