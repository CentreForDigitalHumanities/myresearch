import pytest
from form.models import MRForm, Step, TextQuestion


@pytest.fixture
def test_form() -> MRForm:
    return MRForm.objects.create(name="Test Form")


@pytest.fixture
def test_step(test_form: MRForm) -> Step:
    """Create a test step associated with the test form."""
    return Step.objects.create(name="Test Step", slug="test-step", form=test_form)


@pytest.fixture
def trigger_question(test_step: Step) -> TextQuestion:
    """Create a trigger question for conditions."""
    return TextQuestion.objects.create(
        text="Trigger Question",
        step=test_step,
    )


@pytest.fixture
def target_question(test_step: Step) -> TextQuestion:
    """Create a target question for conditions."""
    return TextQuestion.objects.create(
        text="Target Question",
        step=test_step,
    )
