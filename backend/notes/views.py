from braces import views as braces
from django.views import generic

from .models import Note

class NoteView(braces.LoginRequiredMixin, generic.DetailView):

    template_name = "notes/note.html"
    model = Note
