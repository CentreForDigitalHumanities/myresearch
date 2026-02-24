import pytest

from django.contrib.auth import get_user_model

from form.models import MRForm

User = get_user_model()


@pytest.fixture
def test_user():
    """Create a test user."""
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpass123",
    )


@pytest.fixture
def form() -> MRForm:
    return MRForm.objects.create(name="Test Form")
