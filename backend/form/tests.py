import pytest

from django.db import IntegrityError, transaction

from form.models import MRForm, Step


@pytest.mark.django_db(transaction=True)
def test_database_constraint_prevents_invalid_steps(form: MRForm):
    """Test that the database constraint prevents creating invalid steps."""

    parent_step = Step.objects.create(name="Parent", slug="parent", form=form)

    # Transactions are needed to avoid TransactionManagementError in tests.
    with transaction.atomic():
        # The user should not be able to create a step with both parent and form.
        with pytest.raises(IntegrityError):
            Step.objects.create(
                name="Invalid Step",
                slug="invalid",
                parent=parent_step,
                form=form,
            )

    # The user should not be able to create a step with neither parent nor form.
    with transaction.atomic():
        with pytest.raises(IntegrityError):
            Step.objects.create(
                name="Invalid Step 2",
                slug="invalid2",
                # Neither parent nor form specified
            )


@pytest.mark.django_db(transaction=True)
class TestStepTopForm:
    """Tests for the Step.top_form property."""

    def test_top_level_step_returns_own_form(self, form: MRForm):
        """Test that a top-level step returns its own form."""
        step = Step.objects.create(name="Top Level Step", slug="top-level", form=form)

        assert step.top_form == form

    def test_substep_returns_parent_form(self, form: MRForm):
        """Test that a substep returns its parent's form."""
        parent_step = Step.objects.create(name="Parent Step", slug="parent", form=form)

        substep = Step.objects.create(
            name="Substep", slug="substep", parent=parent_step
        )

        assert substep.top_form == form

    def test_multi_level_nesting_returns_top_form(self, form: MRForm):
        """Test that deeply nested steps return the top-level form."""
        # Create hierarchy: form -> step1 -> step2 -> step3
        step1 = Step.objects.create(name="Step 1", slug="step1", form=form)

        step2 = Step.objects.create(name="Step 2", slug="step2", parent=step1)

        step3 = Step.objects.create(name="Step 3", slug="step3", parent=step2)

        # All steps should return the same top-level form
        assert step1.top_form == step2.top_form == step3.top_form == form

    def test_unsaved_step_raises_error(self, form: MRForm):
        """Test that calling top_form on an unsaved step raises ValueError."""
        step = Step(name="Unsaved Step", slug="unsaved", form=form)

        with pytest.raises(ValueError) as cm:
            _ = step.top_form

        assert "Step must be saved before calling get_form" in str(cm.value)


@pytest.mark.django_db(transaction=True)
class TestAllStepsAllQuestions:
    """Tests for the MRForm.all_steps and MRForm.all_questions methods."""

    def test_all_steps_returns_all_steps(self, form: MRForm):
        """Test that all_steps returns all steps in the form."""
        step1 = Step.objects.create(name="Step 1", slug="step1", form=form)
        step2 = Step.objects.create(name="Step 2", slug="step2", parent=form)
        step3 = Step.objects.create(name="Step 3", slug="step3", parent=form)
        step4 = Step.objects.create(name="Step 4", slug="step4", parent=step1)
        step5 = Step.objects.create(name="Step 5", slug="step5", parent=step2)
        step6 = Step.objects.create(name="Step 6", slug="step6", form=step2)

        all_steps = form.all_steps()

        assert set(all_steps) == {step1, step2, step3, step4, step5, step6}
