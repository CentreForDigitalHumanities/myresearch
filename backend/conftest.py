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


# autouse=True ensures that the Form is saved to the test db.
# This is required for create_study_test.py
@pytest.fixture(autouse=True)
def form(db) -> MRForm:
    return MRForm.objects.create(name="Test Form")
