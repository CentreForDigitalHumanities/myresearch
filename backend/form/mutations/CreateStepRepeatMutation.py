from graphene import ID, InputObjectType, List, Mutation, NonNull, ResolveInfo
from graphene_django.types import ErrorType

from form.models.form import RepeatIndex, Step
from form.models.responses import UserFormSubmission
from main.models import User


class CreateStepRepeatMutationInput(InputObjectType):
    submission_id = ID(required=True)
    step_id = ID(required=True)
    parent_id = ID()


class CreateStepRepeatMutation(Mutation):
    new_repeat_index = ID()
    errors = List(NonNull(ErrorType))

    class Arguments:
        input = CreateStepRepeatMutationInput(required=True)

    @classmethod
    def mutate(
        cls,
        root: None,
        info: ResolveInfo,
        input: CreateStepRepeatMutationInput,
    ):
        user: User = info.context.user

        submission_id = getattr(input, "submission_id")
        parent_id = getattr(input, "parent_id", None)
        step_id = getattr(input, "step_id")

        try:
            repeatable_step = Step.objects.get(is_repeatable=True, pk=step_id)
            submission = UserFormSubmission.objects.get(
                pk=submission_id,
            )
            if parent_id is not None:
                parent_index = RepeatIndex.objects.get(
                    pk=parent_id,
                )
            else:
                parent_index = None
        except Step.DoesNotExist:
            error = ErrorType(
                field="step_id",  # type: ignore
                message=f"Step with id {step_id} does not exist or is not repeatable.",  # type: ignore
            )
            return cls(errors=[error])  # type: ignore
        except UserFormSubmission.DoesNotExist:
            error = ErrorType(
                field="submission_id",  # type: ignore
                message=f"Submission with id {submission_id} does not exist.",  # type: ignore
            )
            return cls(errors=[error])  # type: ignore
        except RepeatIndex.DoesNotExist:
            error = ErrorType(
                field="parent_id",  # type: ignore
                message=f"Parent index with id {parent_id} does not exist.",  # type: ignore
            )
            return cls(errors=[error])  # type: ignore

        try:
            assert submission.can_be_edited_by(user)
        except AssertionError:
            error = ErrorType(
                field="submission_id",  # type: ignore
                message=f"Access denied.",  # type: ignore
            )
            return cls(errors=[error])  # type: ignore

        new_repeat_index = RepeatIndex.objects.create(
            parent=parent_index,
        )
        new_repeat_index.submissions.add(submission)

        repeatable_step.repeat_indices.add(new_repeat_index)

        return cls(
            new_repeat_index=new_repeat_index.pk, # type: ignore
            errors=[], # type: ignore
        )
