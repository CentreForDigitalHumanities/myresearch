from django.test import TestCase
from django.db import IntegrityError, transaction
from .models import MRForm, Step


class StepConstraintTests(TestCase):
    """Tests for the database constraint on the Step model."""

    def setUp(self):
        """Set up test data."""
        self.form = MRForm.objects.create(name="Test Form")

    def test_database_constraint_prevents_invalid_steps(self):
        """Test that the database constraint prevents creating invalid steps."""

        parent_step = Step.objects.create(name="Parent", slug="parent", form=self.form)

        # Transactions are needed to avoid TransactionManagementError in tests.
        with transaction.atomic():
            # Should not be able to create a step with both parent and form
            with self.assertRaises(IntegrityError):
                Step.objects.create(
                    name="Invalid Step",
                    slug="invalid",
                    parent=parent_step,
                    form=self.form,
                )

        # Should not be able to create a step with neither parent nor form
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                Step.objects.create(
                    name="Invalid Step 2",
                    slug="invalid2",
                    # Neither parent nor form specified
                )


class StepTopFormTests(TestCase):
    """Tests for the Step.top_form property."""

    def setUp(self):
        """Set up test data."""
        self.form = MRForm.objects.create(name="Test Form")

    def test_top_level_step_returns_own_form(self):
        """Test that a top-level step returns its own form."""
        step = Step.objects.create(
            name="Top Level Step", slug="top-level", form=self.form
        )

        self.assertEqual(step.top_form, self.form)

    def test_substep_returns_parent_form(self):
        """Test that a substep returns its parent's form."""
        parent_step = Step.objects.create(
            name="Parent Step", slug="parent", form=self.form
        )

        substep = Step.objects.create(
            name="Substep", slug="substep", parent=parent_step
        )

        self.assertEqual(substep.top_form, self.form)

    def test_multi_level_nesting_returns_top_form(self):
        """Test that deeply nested steps return the top-level form."""
        # Create hierarchy: form -> step1 -> step2 -> step3
        step1 = Step.objects.create(name="Step 1", slug="step1", form=self.form)

        step2 = Step.objects.create(name="Step 2", slug="step2", parent=step1)

        step3 = Step.objects.create(name="Step 3", slug="step3", parent=step2)

        # All steps should return the same top-level form
        self.assertEqual(step1.top_form, self.form)
        self.assertEqual(step2.top_form, self.form)
        self.assertEqual(step3.top_form, self.form)

    def test_unsaved_step_raises_error(self):
        """Test that calling top_form on an unsaved step raises ValueError."""
        step = Step(name="Unsaved Step", slug="unsaved", form=self.form)

        with self.assertRaises(ValueError) as cm:
            _ = step.top_form

        self.assertIn("Step must be saved before calling get_form", str(cm.exception))
