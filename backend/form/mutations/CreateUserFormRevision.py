from graphene import List, Mutation, NonNull, ResolveInfo, Boolean, ID
from graphene_django.types import ErrorType

from form.services.create_user_form_revision import create_user_form_revision

class CreateUserFormRevision(Mutation):
    class Arguments:
        submission_id = NonNull(ID)

    ok = Boolean(required=True)
    errors = List(NonNull(ErrorType), required=True)

    @classmethod
    def mutate(
        cls,
        root: None,
        info: ResolveInfo,
        submission_id: str,
    ):
        try:
            create_user_form_revision(submission_id)
        except:
            error = ErrorType(
                messages=[f"Failed to copy UserFormSubmission with id: {submission_id}"]
            )
            return cls(ok=False, errors=[error])

        return cls(ok=True, errors=[])
