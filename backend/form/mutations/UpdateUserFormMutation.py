from graphene import List, Mutation, ResolveInfo, String, Boolean
from graphene_django.types import ErrorType

from form.models import QuestionResponse, UserFormSubmission
from form.mutations.utils.inputs import ResponseInput, UserFormInput
from main.models import User
from research.models import Study


class UpdateUserFormMutation(Mutation):
    class Arguments:
        user_form_input = UserFormInput(required=True)

    ok = Boolean(required=True)
    errors = List(String, required=True)

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
            save_responses(submission.pk, responses)
        except Exception as e:
            error = ErrorType(messages=[f"Answers could not be saved: {str(e)}"])
            return cls(ok=False, errors=[error])  # type: ignore

        if create_study_flag:
            create_study(submission)

        return cls(ok=True, errors=[])  # type: ignore


def get_or_create_submission(
    user: User, user_form_input: UserFormInput
) -> UserFormSubmission:
    submission_id = user_form_input.id
    if not submission_id:
        form_config_id = user_form_input.form_config_id
        return UserFormSubmission.objects.create(user=user, form_id=form_config_id)
    else:
        return UserFormSubmission.objects.get(id=submission_id)


def save_responses(submission_id: str, responses: list[ResponseInput]):
    for response in responses:
        try:
            qr = QuestionResponse.objects.get(id=response.id)
            if qr.answer != response.answer:
                qr.answer = response.answer
                qr.save()
        except QuestionResponse.DoesNotExist:
            print(
                [
                    submission_id,
                    response.question_id,
                    response.repeat_index,
                    response.id,
                ]
            )
            QuestionResponse.objects.create(
                submission_id=submission_id,
                question_id=response.question_id,
                answer=response.answer,
                repeat_index=response.repeat_index,
            )
        except:
            error = ErrorType(messages=["something went wrong ..."])
            return cls(ok=False, errors=[error])  # type: ignore


def create_study(submission: UserFormSubmission) -> None:
    study, created = Study.objects.get_or_create(
        form=submission.form,
        created_by=submission.user,
    )

    if created:
        submission.study = study
        submission.save()

