import pytest

from django.db import IntegrityError, transaction

from form.models import MRForm, Step


@pytest.mark.django_db(transaction=True)
def test_database_constraint_prevents_invalid_steps(form: MRForm):
    """Test that the database constraint prevents creating invalid steps."""

    parent_step = Step.objects.create(name="Parent", slug="parent", form=form)

    # Transactions are needed to avoid TransactionManagementError in tests.
    with transaction.atomic():
        # The user should not be able to create a step with just a parent.
        with pytest.raises(IntegrityError):
            Step.objects.create(
                name="Invalid Step",
                slug="invalid",
                parent=parent_step,
            )


@pytest.mark.django_db(transaction=True)
def test_question_save_sets_form(form: MRForm):
    """Test that the database constraint prevents creating invalid steps."""

    step = Step.objects.create(name="Step", slug="Step", form=form)

    # create will call save()
    tq = TextQuestion.objects.create(
        step=step,
        text="Text 1",
    )

    assert tq.form == step.form

    # Creating a question without saving should allow for no form to be set
    tq2 = TextQuestion(step=step, text="Text 2")

    with pytest.raises(ObjectDoesNotExist):
        _ = tq2.form

    # But it should be set after save()
    tq2.save()

    assert tq2.form == step.form


@pytest.mark.django_db(transaction=True)
class TestAllStepsAllQuestions:
    """Tests for the MRForm.all_steps and MRForm.all_questions methods."""

    def test_all_steps_returns_all_steps(self, form: MRForm):
        """Test that all_steps returns all steps in the form."""
        step1 = Step.objects.create(name="Step 1", slug="step1", form=form)
        step2 = Step.objects.create(name="Step 2", slug="step2", parent=step1)
        step3 = Step.objects.create(name="Step 3", slug="step3", parent=step1)
        step4 = Step.objects.create(name="Step 4", slug="step4", parent=step2)
        step5 = Step.objects.create(name="Step 5", slug="step5", parent=step3)
        step6 = Step.objects.create(name="Step 6", slug="step6", parent=step4)

        all_steps = form.all_steps()

        assert set(all_steps) == {step1, step2, step3, step4, step5, step6}
