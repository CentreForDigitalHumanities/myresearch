from graphene import List, Mutation, NonNull, ResolveInfo, Boolean
from graphene_django.types import ErrorType

from form.mutations.utils.inputs import UserFormInput
from main.models import User
from form.services.update_submission import update_submission
from form.mutations.utils.inputs import UserFormInput
from research.models import Study
from research.other_models.reviews import StatusChange, SubmissionStatus


class UpdateUserFormSubmission(Mutation):
    class Arguments:
        user_form_input = UserFormInput(required=True)
        finalize = Boolean(
            default_value=False,
            description="If true, the status of the study will change to SUBMITTED.",
        )

    ok = Boolean(required=True)
    errors = List(NonNull(ErrorType), required=True)

    @classmethod
    def mutate(
        cls,
        root: None,
        info: ResolveInfo,
        user_form_input: UserFormInput,
        finalize: bool,
    ):
        user: User = info.context.user

        try:
            submission = update_submission(
                user,
                user_form_input,
            )
        except Exception as e:
            error = ErrorType(
                field="responses",
                messages=[str(e)],
            )
            return cls(ok=False, errors=[error])

        study: Study = submission.study  # type: ignore

        if finalize:
            StatusChange.objects.create(
                status=SubmissionStatus.SUBMITTED,
                study_id=study.pk,
                created_by=user,
            )

        return cls(ok=True, errors=[])  # type: ignore
