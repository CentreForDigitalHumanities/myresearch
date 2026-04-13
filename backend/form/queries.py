from typing import Optional
from graphene import ID, Field, ObjectType, ResolveInfo, String


from main.models import User
from form.services.form_evaluator import FormEvaluator
from form.services.user_form_resolver import UserFormResolver
from form.types.UserFormType import UserFormType
from form.models import UserFormSubmission


class FormQueries(ObjectType):
    form = Field(
        UserFormType,
        submission_id=ID(required=True),
        mr_permission=String(required=True),
        description="Retrieves the user's submission for a specific form.",
    )

    @staticmethod
    def resolve_form(
        root, info: ResolveInfo, submission_id: str, mr_permission: str,
    ) -> Optional[UserFormType]:
        user: User = info.context.user
        if not user.is_authenticated:
            return None

        queryset = UserFormSubmission.objects.accessible_objects(user, mr_permission)

        try:
            submission = queryset.get(id=submission_id)
        except UserFormSubmission.DoesNotExist:
            return None

        evaluator = FormEvaluator(submission)
        resolver = UserFormResolver(evaluator)

        return resolver.resolve()
