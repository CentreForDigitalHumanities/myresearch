import pytest

from django.db import IntegrityError, transaction
from django.core.exceptions import ObjectDoesNotExist

from form.models import MRForm, Step, TextQuestion


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
class TestAnnotationKey:
    """Tests for the annotation_key field and its uniqueness constraint."""

    def test_annotation_key_unique_per_form(self, form: MRForm):
        """Test that annotation_key is unique within a form."""
        step = Step.objects.create(name="Step", slug="step", form=form)

        # Create first question with annotation_key
        TextQuestion.objects.create(
            text="Question 1",
            step=step,
            annotation_key="first_question",
        )

        # Creating a second question with the same annotation_key should fail
        with transaction.atomic():
            with pytest.raises(Exception):  # IntegrityError from DB constraint
                TextQuestion.objects.create(
                    text="Question 2",
                    step=step,
                    annotation_key="first_question",
                )

    def test_annotation_key_allowed_in_different_forms(self):
        """Test that the same annotation_key can be used in different forms."""
        form1 = MRForm.objects.create(name="Form 1", version="1.0.0")
        form2 = MRForm.objects.create(name="Form 2", version="1.0.0")

        step1 = Step.objects.create(name="Step 1", slug="step1", form=form1)
        step2 = Step.objects.create(name="Step 2", slug="step2", form=form2)

        # Create questions with same annotation_key in different forms
        q1 = TextQuestion.objects.create(
            text="Question 1",
            step=step1,
            annotation_key="shared_key",
        )
        q2 = TextQuestion.objects.create(
            text="Question 2",
            step=step2,
            annotation_key="shared_key",
        )

        assert q1.annotation_key == q2.annotation_key == "shared_key"
        assert q1.form == form1
        assert q2.form == form2
