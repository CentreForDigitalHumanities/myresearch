import json
import pytest
from io import BytesIO

from django.test import RequestFactory
from django.contrib.auth import get_user_model

from main.models import User
from form.views import FileUploadView, FileDownloadView


@pytest.fixture
def normal_user() -> User:
    return User.objects.create_user(username="user", password="1234")


@pytest.mark.django_db()
class TestFileUpload:
    """Tests for file upload functionality."""

    def test_file_upload_download(self, normal_user):
        """Test that a file can be uploaded successfully."""

        User = get_user_model()
        user = User.objects.create_user(username="testuser", password="testpass")
        factory = RequestFactory()

        upload_view = FileUploadView.as_view()
        download_view = FileDownloadView.as_view()

        dummy_file = BytesIO(b"Dummy file content")
        dummy_file.name = "dummy.txt"

        # First upload the file
        request = factory.post("/upload/", {"file": dummy_file})
        request.user = user

        response = upload_view(request)
        body = json.loads(response.content)
        file_name = body["name"]
        uuid = body["value"]

        assert response.status_code == 201
        assert file_name == "dummy.txt"
        assert uuid is not None

        # Now download the file using the returned UUID and check its content.
        request = factory.get(f"/files/{uuid}/")
        request.user = user

        download_response = download_view(request, uuid=uuid)

        assert download_response.status_code == 200
        assert download_response.content == b"Dummy file content"
