from main.models import User
from form.models import UserFormSubmission, QuestionResponse
from form.mutations.utils.inputs import UserFormInput


def update_or_create_submission(
    user: User, user_form_input: UserFormInput
) -> UserFormSubmission:
    submission_id = getattr(user_form_input, "submission_id", None)
    form_config_id = getattr(user_form_input, "form_config_id", None)

    if submission_id:
        current_submission = UserFormSubmission.objects.get(id=submission_id)
    else:
        current_submission = UserFormSubmission.objects.create(
            user=user, form_id=form_config_id
        )

    for response in getattr(user_form_input, "responses", []):
        response_id = response["id"] if "id" in response else None
        if response_id:
            # See if the response already exists
            qr = QuestionResponse.objects.get(id=response["id"])
            # Check if new answer differs from the answer in the DB
            if qr.answer != response["answer"]:
                # Check if this response is used for multiple submissions
                # AKA this is a revision
                if qr.submissions.count() > 1:
                    # Remove the old response from this submission
                    current_submission.responses.remove(qr)
                    # Create a new response
                    new_response = QuestionResponse.objects.create(
                        question_id=response["question_id"],
                        answer=response["answer"],
                        repeat_index=response["repeat_index"],
                    )
                    new_response.submissions.add(current_submission)
                else:
                    # If this is not a revision, just update the answer
                    qr.answer = response["answer"]
                    qr.save()
        else:
            new_response = QuestionResponse.objects.create(
                question_id=response["question_id"],
                answer=response["answer"],
                repeat_index=response["repeat_index"],
            )
            new_response.submissions.add(current_submission)

    return current_submission
