from form.models.questions import FileUploadQuestion
from main.models import MRPermission, User
from graphene_django.types import ErrorType
from form.models.responses import MRDocument
from form.mutations.utils.inputs import UserFormInput
from django.utils import timezone
from form.models import (
    UserFormSubmission,
    QuestionResponse,
    BaseQuestion,
)


def _delete_document_if_cleared(old_answer: dict, new_answer: dict) -> None:
    """
    Delete the MRDocument when a FileUpload answer is cleared.
    """
    old_uuid = old_answer.get("value", "") if isinstance(old_answer, dict) else ""
    new_uuid = new_answer.get("value", "") if isinstance(new_answer, dict) else ""
    if old_uuid and not new_uuid:
        try:
            MRDocument.objects.get(file__uuid=old_uuid).delete()
        except MRDocument.DoesNotExist:
            pass


def update_submission(
    user: User, user_form_input: UserFormInput, finalize: bool = False
) -> tuple[UserFormSubmission, list[ErrorType]]:
    # Usually we can use user_form_input.submission_id or getattr(user_form_input, "submission_id").
    # This breaks the tests, however, where user_form_input is mocked as a dict.
    # That is why we use .get() here, which handles both cases.
    try:
        # first filter for editable objects, and then try to get the specific submission
        current_submission: (
            UserFormSubmission
        ) = UserFormSubmission.objects.accessible_objects(user, MRPermission.EDIT).get(
            id=user_form_input.get("submission_id"),
        )
    except UserFormSubmission.DoesNotExist:
        raise Exception(
            f"Submission with id {user_form_input.get('submission_id')} "
            f"belonging to user {user} does not exist."
        )

    errors: list[ErrorType] = []

    for response in user_form_input.get("responses", []):  # type: ignore
        response_id = response["id"] if "id" in response else None

        # Responses need to be validated but only once the responses are final.
        if finalize:
            try:
                validate_response(response)
            except Exception as e:
                # if responses cause an error, add an error to the mutation's response
                question_id = response.get("question_id", "<unknown>")
                errors.append(
                    ErrorType(
                        field="responses",
                        messages=[f"Invalid response for question {question_id}: {e}"],
                    )
                )
                # We don't save responses that do not pass validation
                continue

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
                    if response["answer"]["value"] == "" and isinstance(
                        qr.question.get_subclass(), FileUploadQuestion
                    ):
                        _delete_document_if_cleared(qr.answer, response["answer"])
                    # If this is not a revision, just update the answer
                    qr.answer = response["answer"]
                    qr.save()

                current_submission.updated_at = timezone.now()
        else:
            new_response = QuestionResponse.objects.create(
                question_id=response["question_id"],
                answer=response["answer"],
                repeat_index=response["repeat_index"],
            )
            new_response.submissions.add(current_submission)
            current_submission.updated_at = timezone.now()
    current_submission.save()
    return current_submission, errors


def validate_response(response):
    """Backend validation incase malicious responses. Under normal circumstances all validations are already checked in the frontend"""
    question = BaseQuestion.objects.get(id=response["question_id"]).get_subclass()
    # validate will throw an error in case of wrong input.
    question.validate(response["answer"]["value"])
