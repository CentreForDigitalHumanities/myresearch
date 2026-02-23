from graphene import List, Mutation, NonNull, ResolveInfo, String, Boolean
from graphene_django.types import ErrorType

from form.services.update_submission import update_or_create_submission
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

        try:
            update_or_create_submission(
                info.context.user,
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

        return cls(ok=True, errors=[])
