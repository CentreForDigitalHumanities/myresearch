from graphene import List, Mutation, NonNull, ResolveInfo, String, Boolean
from graphene_django.types import ErrorType

from form.models import QuestionResponse, UserFormSubmission
from form.mutations.utils.inputs import UserFormInput


class UpdateUserFormSubmission(Mutation):
    class Arguments:
        user_form_input = UserFormInput(required=True)

    ok = Boolean(required=True)
    errors = List(NonNull(ErrorType), required=True)

    @classmethod
    def mutate(
        cls,
        root: None,
        info: ResolveInfo,
        user_form_input: UserFormInput,
    ):
        if not getattr(user_form_input, "submission_id", None):
            current_submission = UserFormSubmission.objects.create(
                user=info.context.user, form_id=user_form_input["form_config_id"]
            )
        else:
            current_submission = UserFormSubmission.objects.get(
                id=user_form_input["submission_id"]
            )

        for response in getattr(user_form_input, "responses", []):
            try:
                # See if the response already exists
                qr = QuestionResponse.objects.get(id=response.id)
                # Check if new answer differs from the answer in the DB
                if qr.answer != response.answer:
                    # Check if this response is used for multiple submissions
                    # AKA this is a revision
                    if qr.submissions.count() > 1:
                        # Remove the old response from this submission
                        current_submission.responses.remove(qr)
                        # Create a new response
                        QuestionResponse.objects.create(
                            submission=current_submission,
                            question_id=response.question_id,
                            answer=response.answer,
                            repeat_index=response.repeat_index,
                        )
                    else:
                        # If this is not a revision, just update the answer
                        qr.answer = response.answer
                        qr.save()
            except QuestionResponse.DoesNotExist:
                new_reponse = QuestionResponse.objects.create(
                    question_id=response.question_id,
                    answer=response.answer,
                    repeat_index=response.repeat_index,
                )
                new_reponse.submissions.add(current_submission)
            except Exception as e:
                error = ErrorType(
                    field="responses",
                    messages=[
                        f"Failed to save responses for UserFormSubmission with id: {getattr(user_form_input, 'id', None)}"
                    ]
                )
                return cls(ok=False, errors=[error])

        return cls(ok=True, errors=[])
