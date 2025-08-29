from modeltranslation.translator import register, TranslationOptions

from .models import (
    DateQuestion,
    FileUploadQuestion,
    MRForm,
    NumberQuestion,
    SelectOption,
    Step,
    StepInfoQuestion,
    StepInfoText,
    TextQuestion,
    SelectQuestion,
    TrueFalseQuestion,
)


@register(MRForm)
class FormTranslationOptions(TranslationOptions):
    fields = ["name", "description"]


@register(Step)
class StepTranslationOptions(TranslationOptions):
    fields = ["name", "description"]


@register(StepInfoQuestion)
class StepInfoQuestionTranslationOptions(TranslationOptions):
    fields = ["text"]


@register(StepInfoText)
class StepInfoTextTranslationOptions(TranslationOptions):
    fields = ["text"]


@register(SelectOption)
class SelectOptionTranslationOptions(TranslationOptions):
    fields = ["label"]


@register(SelectQuestion)
class SelectQuestionTranslationOptions(TranslationOptions):
    fields = ["text", "description"]


@register(TrueFalseQuestion)
class TrueFalseQuestionTranslationOptions(TranslationOptions):
    fields = ["text", "description"]


@register(TextQuestion)
class TextQuestionTranslationOptions(TranslationOptions):
    fields = ["text", "description", "placeholder"]


@register(NumberQuestion)
class NumberQuestionTranslationOptions(TranslationOptions):
    fields = ["text", "description"]


@register(DateQuestion)
class DateQuestionTranslationOptions(TranslationOptions):
    fields = ["text", "description"]


@register(FileUploadQuestion)
class FileUploadQuestionTranslationOptions(TranslationOptions):
    fields = ["text", "description"]
