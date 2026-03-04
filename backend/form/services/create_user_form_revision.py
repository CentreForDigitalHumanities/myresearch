from form.models import UserFormSubmission


def create_user_form_revision(submission_id: str) -> UserFormSubmission:
    """
    Util function to copy a UserFormSubmission, used for revisions.

    :param submission_id: ID of the submission to be copied
    :type submission_id: int
    """
    old_submission = UserFormSubmission.objects.get(id=submission_id)
    new_submission = UserFormSubmission.objects.create(
        user=old_submission.user, form=old_submission.form, study=old_submission.study
    )
    new_submission.responses.set(old_submission.responses.all())

    return new_submission
