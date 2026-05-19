from django.http import JsonResponse, HttpResponseNotFound, HttpResponseForbidden
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from cdh.files.views import BaseFileView

from .models.responses import MRDocument, QuestionResponse


class FileUploadView(LoginRequiredMixin, View):
    """Accept a file upload and return the MRDocument PK for use in answers."""

    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES.get("file")
        if not uploaded_file:
            return JsonResponse({"error": "No file provided."}, status=400)

        document = MRDocument()
        document.file = uploaded_file
        document.save()

        return JsonResponse(
            {"value": document.pk, "uuid": str(document.file.uuid)}, status=201
        )


class FileDownloadView(LoginRequiredMixin, BaseFileView):
    """Serve a file identified by its cdh File UUID.

    Access is granted to the submitting user, privacy officers and FETC members.
    """

    def get(self, request, **kwargs):
        if self._file_wrapper is None:
            return HttpResponseNotFound()

        uuid = self.kwargs.get(self.uuid_path_parameter)
        try:
            document = MRDocument.objects.get(file__uuid=uuid)
        except MRDocument.DoesNotExist:
            return HttpResponseNotFound()

        user = request.user
        if not (user.is_privacy_officer or user.is_fetc_member):
            has_access = QuestionResponse.objects.filter(
                answer__value=document.pk,
                submissions__user=user,
            ).exists()
            if not has_access:
                return HttpResponseForbidden()

        return super().get(request, **kwargs)
