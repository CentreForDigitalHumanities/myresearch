from modeltranslation.translator import register, TranslationOptions

from .models import (
    BaseQuestion,
    DateQuestion,
    FileUploadQuestion,
    FormInfoText,
    MRForm,
    NumberQuestion,
    SelectOption,
    FormInfoQuestion,
    TextQuestion,
    SelectQuestion,
    TrueFalseQuestion,
)


@register(MRForm)
class FormTranslationOptions(TranslationOptions):
    fields = ["name", "description"]


@register(FormInfoQuestion)
class FormInfoQuestionTranslationOptions(TranslationOptions):
    fields = ["text"]


@register(FormInfoText)
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


@register(NumberQuestion)
class NumberQuestionTranslationOptions(TranslationOptions):
    pass


@register(DateQuestion)
class DateQuestionTranslationOptions(TranslationOptions):
    pass


@register(FileUploadQuestion)
class FileUploadQuestionTranslationOptions(TranslationOptions):
    pass
