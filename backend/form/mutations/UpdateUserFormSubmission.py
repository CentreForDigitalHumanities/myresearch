from graphene import List, Mutation, NonNull, ResolveInfo, Boolean
from graphene_django.types import ErrorType

from form.models import QuestionResponse, UserFormSubmission
from form.mutations.utils.inputs import ResponseInput, UserFormInput
from main.models import User
from research.models import Study
from form.services.update_submission import update_submission
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

        try:
            update_submission(
                user,
                user_form_input,
            )
        except Exception as e:
            error = ErrorType(
                field="responses",
                messages=[str(e)],
            )
            return cls(ok=False, errors=[error])

        return cls(ok=True, errors=[])  # type: ignore
