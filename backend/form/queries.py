from typing import Optional
from graphene import ID, Field, ObjectType, ResolveInfo


from form.services.form_evaluator import FormEvaluator
from form.types.UserFormType import UserFormResolver, UserFormType
from form.types.MRFormType import MRFormType
from form.models import MRForm, Step


class FormQueries(ObjectType):
    user_form = Field(
        UserFormType,
        description="Retrieves the user's submission for a specific form.",
    )

    @staticmethod
    def resolve_user_form(root, info: ResolveInfo) -> Optional[UserFormType]:
        user = info.context.user
        if not user.is_authenticated:
            return None

        # Get the latest form template (for testing purposes only)
        form = MRForm.objects.order_by("-created_at").first()

        if not form:
            return None

        evaluator = FormEvaluator(form, user)
        resolver = UserFormResolver(evaluator)
        return resolver.resolve()
