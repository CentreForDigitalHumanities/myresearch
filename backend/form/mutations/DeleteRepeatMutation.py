from graphene import Boolean, InputObjectType, List, Mutation, NonNull, ResolveInfo, ID
from graphene_django.types import ErrorType

from main.models import User
from form.models import (
    RepeatIndex,
    UserFormSubmission,
)


class DeleteRepeatMutationInput(InputObjectType):
    submission_id = ID(required=True)
    repeat_index_id = ID(required=True)


class DeleteRepeatMutation(Mutation):
    errors = List(NonNull(ErrorType), required=True)
    ok = Boolean(required=True)

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

        submission_id = getattr(input, "submission_id")
        repeat_index_id = getattr(input, "repeat_index_id")

        try:
            repeat_index = RepeatIndex.objects.get(
                pk=repeat_index_id,
            )
            submission = UserFormSubmission.objects.get(
                pk=submission_id,
            )
        except RepeatIndex.DoesNotExist:
            error = ErrorType(
                field="repeat_index_id",  # type: ignore
                message=f"RepeatIndex with id {repeat_index_id} does not exist.",  # type: ignore
            )
            return cls(ok=False, errors=[error])  # type: ignore
        except UserFormSubmission.DoesNotExist:
            error = ErrorType(
                field="submission_id",  # type: ignore
                message=f"Submission with id {submission_id} does not exist.",  # type: ignore
            )
            return cls(ok=False, errors=[error])  # type: ignore

        repeat_index.submissions.remove(submission)
        try:
            assert submission.can_be_edited_by(user)
        except AssertionError:
            error = ErrorType(
                field="submission_id",  # type: ignore
                message=f"Access denied.",  # type: ignore
            )
            return cls(ok=False, errors=[error])  # type: ignore

        # When a repeat index is removed from its last submission, it
        # is deleted. Currently we do not delete all child indices that
        # may exist beneath it, e.g. a repeatable question within a
        # repeatable step. But this would be the place to do so.
        if repeat_index.submissions.count() == 0:
            repeat_index.delete()

        return cls(ok=True, errors=[])  # type: ignore
