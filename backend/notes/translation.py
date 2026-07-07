from modeltranslation.translator import register, TranslationOptions

from .models import (
    Note,
)


@register(Note)
class NoteTranslationOptions(TranslationOptions):
    fields = ["title", "content"]
