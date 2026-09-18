from graphene import Boolean, InputObjectType, List, Mutation, NonNull, ResolveInfo, ID
from graphene_django.types import ErrorType
from django.core.exceptions import ObjectDoesNotExist

from main.models import User
from form.models import (
    RepeatIndex,
    UserFormSubmission,
)


class DeleteRepeatMutationInput(InputObjectType):
    user_form_id = ID(required=True)
    repeat_index_id = ID(required=True)


class DeleteRepeatMutation(Mutation):
    errors = List(NonNull(ErrorType), required=True)
    ok = Boolean(required=False)

    class Arguments:
        input = DeleteRepeatMutationInput(required=True)

    @classmethod
    def mutate(
        cls,
        root: None,
        info: ResolveInfo,
        input: DeleteRepeatMutationInput,
    ):
        user: User = info.context.user

        user_form_id = getattr(input, "user_form_id")
        repeat_index_id = getattr(input, "repeat_index_id")

        try:
            repeat_index = RepeatIndex.objects.get(
                pk=repeat_index_id,
            )
            submission = UserFormSubmission.objects.get(
                pk=user_form_id,
            )

            repeat_index.submissions.remove(submission)

        except ObjectDoesNotExist as error:
            return cls(ok=False, errors=[error])
        except Exception as error:
            return cls(ok=False, errors=[error])

        try:
            assert submission.can_be_edited_by(user)
        except AssertionError:
            error = "Access denied"
            return cls(ok=False, errors=[error])

        # When a repeat index is removed from its last submission, it
        # is deleted. Currently we do not delete all child indices that
        # may exist beneath it, e.g. a repeatable question within a
        # repeatable step. But this would be the place to do so.
        if repeat_index.submissions.count() == 0:
            repeat_index.delete()

        return cls(errors=[], ok=True)
