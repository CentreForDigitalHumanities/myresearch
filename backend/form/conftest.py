import pytest
from form.models import MRForm, Step, TextQuestion


@pytest.fixture
def step(form: MRForm) -> Step:
    """Create a test step associated with the test form."""
    return Step.objects.create(name="Test Step", slug="test-step", form=form)


@pytest.fixture
def trigger_question(step: Step) -> TextQuestion:
    """Create a trigger question for conditions."""
    return TextQuestion.objects.create(
        text="Trigger Question",
        step=step,
    )


@pytest.fixture
def target_question(step: Step) -> TextQuestion:
    """Create a target question for conditions."""
    return TextQuestion.objects.create(
        text="Target Question",
        step=step,
    )


@pytest.fixture
def response_input(trigger_question: TextQuestion) -> dict:
    """Create an empty ResponseInput"""
    return {
        "question_id": trigger_question.pk,
        "repeat_index": 0,
        "answer": {"value": None},
    }


@pytest.fixture
def user_form_input(form: MRForm, response_input: dict) -> dict:
    """Create an empty UserFormInput"""
    return {"form_config_id": form.pk, "responses": [response_input]}
