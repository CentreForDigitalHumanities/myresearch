from django.db import models
from django.utils.text import slugify

class Note(models.Model):
    """
    A very barebones model, which can hold html-formatted text, created in the
    admin interface using TinyMCE
    """

    title = models.CharField("Note title", max_length=30)
    content = models.TextField("Note content",
                               help_text="For links to other pages within the "
                               "MR, format url like '/notes/1/'. For links, "
                               "to other websites, format url like 'https://www.uu.nl'. "
                               "In case of a really long word, that is overflowing the formatting, "
                               "go into the source and add the bootstrap class 'text-break' to "
                               "the paragraph in question.",
                               )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        help_text="Used in the URL, will be generated if not provided",
        blank=True,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
