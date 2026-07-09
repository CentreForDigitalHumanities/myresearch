from django.urls import path

from . import views

app_name = "form"

urlpatterns = [
    path("upload/", views.FileUploadView.as_view(), name="file-upload"),
    path("files/<uuid:uuid>/", views.FileDownloadView.as_view(), name="file-download"),
]
