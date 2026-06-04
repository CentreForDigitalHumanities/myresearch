from django.db import models

class Note(models.Model):
    """
    A very barebones model, which can hold html-formatted text, created in the
    admin interface using TinyMCE
    """

    title = models.CharField("Note title", max_length=30)
    content = models.TextField("Note content",
                               help_text="For links to other pages within the "
                               "grant-tool, format url like '/notes/1/'. For links, "
                               "to other websites, format url like 'https://www.uu.nl'. "
                               "In case of a really long word, that is overflowing the formatting, "
                               "go into the source and add the bootstrap class 'text-break' to "
                               "the paragraph in question.",
                               )
