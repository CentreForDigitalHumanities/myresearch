from graphene import List, Mutation, NonNull, ResolveInfo, Boolean
from graphene_django.types import ErrorType

from form.models import QuestionResponse, UserFormSubmission
from form.mutations.utils.inputs import ResponseInput, UserFormInput
from main.models import User
from research.models import Study
from form.services.update_submission import update_or_create_submission
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
        user: User = info.context.user
        submission = get_or_create_submission(user, user_form_input)

        responses = getattr(user_form_input, "responses", [])
        create_study_flag = getattr(user_form_input, "create_study", False)

        try:
            update_or_create_submission(
                user,
                user_form_input,
            )
        except Exception as e:
            error = ErrorType(
                field="responses",
                messages=[
                    f"Failed to save responses for UserFormSubmission with id: {getattr(user_form_input, 'id', None)}"
                ],
            )
            return cls(ok=False, errors=[error])

        try:
            save_responses(submission.pk, responses)
        except Exception as e:
            error = ErrorType(messages=[f"Answers could not be saved: {str(e)}"])
            return cls(ok=False, errors=[error])  # type: ignore

        if create_study_flag:
            create_study(submission)

        return cls(ok=True, errors=[])  # type: ignore


def create_study(submission: UserFormSubmission) -> None:
    study, created = Study.objects.get_or_create(
        form=submission.form,
        created_by=submission.user,
    )

    if created:
        submission.study = study
        submission.save()


def save_responses(submission_id: str, responses: list[ResponseInput]):
    for response in responses:
        try:
            qr = QuestionResponse.objects.get(id=response.id)
            if qr.answer != response.answer:
                qr.answer = response.answer
                qr.save()
        except QuestionResponse.DoesNotExist:
            QuestionResponse.objects.create(
                submission_id=submission_id,
                question_id=response.question_id,
                answer=response.answer,
                repeat_index=response.repeat_index,
            )
        except:
            error = ErrorType(
                messages=[
                    f"Failed to save responses for UserFormSubmission with id: {submission_id}"
                ]
            )
            return cls(ok=False, errors=[error])  # type: ignore
