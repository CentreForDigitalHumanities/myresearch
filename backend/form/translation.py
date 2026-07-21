from modeltranslation.translator import register, TranslationOptions

from .models import (
    BaseQuestion,
    DateQuestion,
    FileUploadQuestion,
    StepInfoText,
    MRForm,
    Step,
    StepInfo,
    NumberQuestion,
    SelectOption,
    TextQuestion,
    SelectQuestion,
    TrueFalseQuestion,
)


@register(MRForm)
class MRFormTranslationOptions(TranslationOptions):
    fields = ["name"]


@register(Step)
class StepTranslationOptions(TranslationOptions):
    fields = ["name", "description"]


@register(StepInfoText)
class FormInfoTextTranslationOptions(TranslationOptions):
    fields = ["text"]


@register(StepInfo)
class StepInfoTranslationOptions(TranslationOptions):
    fields = ["text", "content"]


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


@register(NumberQuestion)
class NumberQuestionTranslationOptions(TranslationOptions):
    pass


@register(DateQuestion)
class DateQuestionTranslationOptions(TranslationOptions):
    pass


@register(FileUploadQuestion)
class FileUploadQuestionTranslationOptions(TranslationOptions):
    pass
