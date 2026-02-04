from graphene import List, Mutation, NonNull, ResolveInfo, String, Boolean
from graphene_django.types import ErrorType

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
        if not user_form_input["id"]:
            submission = UserFormSubmission.objects.create(
                user=info.context.user, form_id=user_form_input["form_config_id"]
            )
        else:
            submission = UserFormSubmission.objects.get(id=user_form_input["id"])

        for response in user_form_input["responses"]:
            try:
                qr = QuestionResponse.objects.get(id=response.id)
                if qr.answer != response.answer:
                    qr.answer = response.answer
                    qr.save()
            except QuestionResponse.DoesNotExist:
                QuestionResponse.objects.create(
                    submission=submission,
                    question_id=response.question_id,
                    answer=response.answer,
                    repeat_index=response.repeat_index,
                )
            except:
                error = ErrorType(messages=["something went wrong ..."])
                return cls(ok=False, errors=[error])

        return cls(ok=True, errors=[])
