from typing import Optional
from graphene import ID, Field, ObjectType, ResolveInfo


from main.models import User
from form.services.form_evaluator import FormEvaluator
from form.services.user_form_resolver import UserFormResolver
from form.types.UserFormType import UserFormType
from form.models import UserFormSubmission


class FormQueries(ObjectType):
    form = Field(
        UserFormType,
        submission_id=ID(required=True),
        description="Retrieves the user's submission for a specific form.",
    )

    @staticmethod
    def resolve_form(
        root, info: ResolveInfo, submission_id: int
    ) -> Optional[UserFormType]:
        user: User = info.context.user
        if not user.is_authenticated:
            return None

        # TODO: implement permissions
        submission = UserFormSubmission.objects.get(id=submission_id)

        evaluator = FormEvaluator(submission)
        resolver = UserFormResolver(evaluator)

        return resolver.resolve()
