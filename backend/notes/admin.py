from django.contrib import admin
from django.db import models
from cdh.core.forms import TinyMCEWidget
from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    """
    A bit of a copy of the admin interface for cdh.core.systemmessages
    """

    fields = [
        "title_nl",
        "title_en",
        "content_nl",
        "content_en",
        "slug",
    ]

    class Media:
        js = (
            "cdh.core/js/jquery-3.6.1.min.js",
            "cdh.core/js/tinymce/tinymce.min.js",
            "cdh.core/js/tinymce/tinymce-jquery.min.js",
            "cdh.core/js/tinymce/shim.js",
        )

    formfield_overrides = {
        models.TextField: {"widget": TinyMCEWidget},
    }

    list_display = ("title_nl", "title_en")
    search_fields = (
        "title_nl",
        "title_en",
    )
