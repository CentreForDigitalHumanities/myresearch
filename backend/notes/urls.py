
from django.urls import path

from .views import NoteView

app_name = 'notes'

urlpatterns = [
    path('<int:pk>/', NoteView.as_view(), name='note'),
]