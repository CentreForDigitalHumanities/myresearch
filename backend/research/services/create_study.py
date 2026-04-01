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
    submission = UserFormSubmission.objects.create(
        user=user,
        form=latest_form,
    )
    submission.save()
    
    # Create a study
    study = Study(created_by=user)
    study.save()
    
    # Create a StatusChange
    status_change = StatusChange.objects.create(
        status=SubmissionStatus.DRAFT, created_by=user, study=study
    )
    status_change.save()
    
    # Link the study to the submission
    submission.study = study
    submission.save()
    
    return study
