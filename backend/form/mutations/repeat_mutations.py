from form.models.responses import QuestionResponse
from main.models import MRPermission, User
from form.models import (
    Repeatable,
    RepeatIndex,
    UserFormSubmission,
    RepeatableStepQuestion,
)

from graphene import Boolean, List, Mutation, ResolveInfo, ID
from graphene_django.types import ErrorType
from django.core.exceptions import ObjectDoesNotExist


class CreateRepeatMutation(Mutation):

    class Arguments:
        user_form_id = ID(required=True)
        repeatable_id = ID(required=True)
        parent_id = ID(required=False)
        response_id = ID(required=False)

    new_repeat_index = ID()
    errors = List(ErrorType)

    @classmethod
    def mutate(
        cls,
        root: None,
        info: ResolveInfo,
        user_form_id: int,
        repeatable_id: int,
        parent_id: int = None,
        response_id: int = None,
    ):
        user: User = info.context.user

        try:
            base_repeat = Repeatable.objects.get(
                pk=repeatable_id,
            )
            submission = UserFormSubmission.objects.get(
                pk=user_form_id,
            )
            if parent_id is not None:
                parent_index = RepeatIndex.objects.get(
                    pk=parent_id,
                )
            else:
                parent_index = None
            # assert submission.can_be_edited_by(user)
        except ObjectDoesNotExist as error:
            return cls(errors=[error])
        except AssertionError:
            error = "Access denied"
            return cls(errors=[error])

        new_repeat = RepeatIndex(
            parent=parent_index,
        )
        new_repeat.save()
        new_repeat.submissions.add(submission)
        base_repeat.repeat_indices.add(
            new_repeat,
        )

        try:
            rsq = RepeatableStepQuestion.objects.get(repeatable_step=repeatable_id)
        except RepeatableStepQuestion.MultipleObjectsReturned as error:
            return cls(errors=[error])

        # Use a QuestionResponse to store
        if response_id is not None:
            qr = QuestionResponse.objects.get(
                pk=response_id,
            )
        else:
            qr = QuestionResponse.objects.create(question=rsq, answer={"value": []})
            qr.submissions.add(submission)

        answer_value = qr.answer["value"]
        answer_value.append(new_repeat.pk)
        qr.answer = {"value": answer_value}
        qr.save()

        return cls(
            new_repeat_index=new_repeat.pk,
            errors=[],
        )


class DeleteRepeatMutation(Mutation):

    class Arguments:
        user_form_id = ID(required=True)
        repeat_id = ID(required=True)
        response_id = ID(required=True)

    errors = List(ErrorType)
    ok = Boolean(required=False)

    @classmethod
    def mutate(
        cls,
        root: None,
        info: ResolveInfo,
        user_form_id: int,
        repeat_id: int,
        response_id: int,
    ):
        user: User = info.context.user

        try:
            repeat_index = RepeatIndex.objects.get(
                pk=repeat_id,
            )
            submission = UserFormSubmission.objects.get(
                pk=user_form_id,
            )
            assert submission in UserFormSubmission.objects.accessible_objects(
                user, MRPermission.EDIT
            )

            repeat_index.submissions.remove(
                submission,
            )
        except ObjectDoesNotExist as error:
            return cls(ok=False, errors=[error])
        except AssertionError:
            error = "Access denied"
            return cls(ok=False, errors=[error])
        except Exception as error:
            return cls(ok=False, errors=[error])

        try:
            qr = QuestionResponse.objects.get(
                pk=response_id,
            )
            # Remove the repeat_id from the answer value list
            answer_value = qr.answer.get("value", [])
            repeat_id = int(repeat_id)
            if repeat_id in answer_value:
                answer_value.remove(repeat_id)
                qr.answer = {"value": answer_value}
                qr.save()
        except ObjectDoesNotExist:
            # If we can't find the response, continue
            # The repeat will still be deleted from submissions
            pass

        # When a repeat index is removed from its last submission, it
        # is deleted. Currently we do not delete all child indexes that
        # may exist beneath it, e.g. a repeatable question within a
        # repeatable step. But this would be the place to do so.
        if repeat_index.submissions.count() == 0:
            repeat_index.delete()

        return cls(errors=[], ok=True)
