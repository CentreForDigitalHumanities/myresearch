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
        responses = getattr(user_form_input, "responses", [])
        create_study_flag = getattr(user_form_input, "create_study", False)

        try:
            submission = update_or_create_submission(
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

        if create_study_flag:
            create_study(submission)

        return cls(ok=True, errors=[])  # type: ignore


def create_study(submission: UserFormSubmission) -> None:
    study = Study.objects.create(
        created_by=submission.user,
    )
    submission.study = study
    submission.save()
