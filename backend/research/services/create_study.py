from django.db import transaction

from main.models import User
from form.models import MRForm, UserFormSubmission
from research.models import Study
from research.other_models.reviews import StatusChange, SubmissionStatus


def create_study(user: User) -> Study:
    """
    Create a new study for the given user.

    This service function handles the creation of a study along with its associated
    form submission and initial status change.
    """
    # Create a submission using the latest form
    latest_form = MRForm.objects.all().last()
    if latest_form is None:
        raise ValueError(
            "No MRForm instances exist; cannot create UserFormSubmission without a form."
        )
    # Ensure no partial data gets left behind
    with transaction.atomic():
        # Create a study
        study = Study(created_by=user)
        study.save()

        submission = UserFormSubmission.objects.create(
            user=user,
            form=latest_form,
            study=study,
        )
        submission.save()

        # Create a StatusChange
        status_change = StatusChange.objects.create(
            status=SubmissionStatus.DRAFT, created_by=user, study=study
        )
        status_change.save()

    return study
