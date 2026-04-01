from main.models import User
from form.models import UserFormSubmission, QuestionResponse
from form.mutations.utils.inputs import UserFormInput


def update_submission(user: User, user_form_input: UserFormInput) -> UserFormSubmission:
    # Usually we can use user_form_input.submission_id or getattr(user_form_input, "submission_id").
    # This breaks the tests, however, where user_form_input is mocked as a dict.
    # That is why we use .get() here, which handles both cases.

    current_submission = UserFormSubmission.objects.get(
        id=user_form_input.get("submission_id")
    )

    for response in user_form_input.get("responses", []):  # type: ignore
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
