from graphene import Enum, InputObjectType, List, Mutation, NonNull, ResolveInfo, ID
from graphene_django.types import ErrorType
from django.core.exceptions import ObjectDoesNotExist

from main.models import User
from form.models import (
    BaseQuestion,
    Step,
    RepeatIndex,
    UserFormSubmission,
)


class Repeatable(Enum):
    QUESTION = "question"
    STEP = "step"


class CreateRepeatMutationInput(InputObjectType):
    submission_id = ID(required=True)
    repeatable_type = Repeatable(required=True)
    object_id = ID(required=True)  #  The Step or Question ID
    parent_id = ID()


class CreateRepeatMutation(Mutation):
    new_repeat_index = ID()
    errors = List(NonNull(ErrorType))

    class Arguments:
        input = CreateRepeatMutationInput(required=True)

    @classmethod
    def mutate(
        cls,
        root: None,
        info: ResolveInfo,
        input: CreateRepeatMutationInput,
    ):
        user: User = info.context.user

        submission_id = getattr(input, "submission_id")
        parent_id = getattr(input, "parent_id", None)

        object_id = getattr(input, "object_id")
        object_type = getattr(input, "repeatable_type")
        if object_type == Repeatable.QUESTION:
            RepeatableModel = BaseQuestion
        elif object_type == Repeatable.STEP:
            RepeatableModel = Step
        else:
            error = ErrorType(
                field="repeatable_type",
                message=f"Invalid repeatable_type: {object_type}",
            )
            return cls(errors=[error])

        try:
            repeatable_object = RepeatableModel.objects.get(pk=object_id)
            submission = UserFormSubmission.objects.get(
                pk=submission_id,
            )
            if parent_id is not None:
                parent_index = RepeatIndex.objects.get(
                    pk=parent_id,
                )
            else:
                parent_index = None
        except ObjectDoesNotExist as error:
            return cls(errors=[error])

        try:
            assert submission.can_be_edited_by(user)
        except AssertionError:
            error = "Access denied"
            return cls(errors=[error])

        new_repeat_index = RepeatIndex.objects.create(
            parent=parent_index,
        )
        new_repeat_index.submissions.add(submission)

        repeatable_object.repeat_indices.add(new_repeat_index)

        return cls(
            new_repeat_index=new_repeat_index.pk,
            errors=[],
        )
