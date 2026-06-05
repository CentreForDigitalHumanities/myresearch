from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from django.urls import reverse

from cdh.core.forms import TinyMCEWidget

from .models import Note

class NoteAdmin(admin.ModelAdmin):

    """
    A bit of a copy of the Grand-Tool which is a bit of a copy of the admin interface for cdh.core.systemmessages
    """

    class Media:
        js = (
            'cdh.core/js/jquery-3.6.1.min.js',
            'cdh.core/js/tinymce/tinymce.min.js',
            'cdh.core/js/tinymce/tinymce-jquery.min.js',
            'cdh.core/js/tinymce/shim.js',
        )
    formfield_overrides = {
        models.TextField: {"widget": TinyMCEWidget},
    }

    @admin.display(description="Note URL")
    def note_link(self, obj):
        return format_html(
            "<a href='{url}' target='_blank'>View Note</a>".format(
                url = reverse(
                    "notes:note",
                    kwargs={"pk":obj.pk},
                )
            )
        )

    list_display = ('slug',)
    search_fields = ('title', 'slug', 'content',)

admin.site.register(Note, NoteAdmin)