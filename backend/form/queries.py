from typing import Optional
from graphene import Field, ObjectType, ResolveInfo


from form.services.form_evaluator import FormEvaluator
from form.types.UserFormType import UserFormResolver, UserFormType
from form.models import MRForm


class FormQueries(ObjectType):
    form = Field(
        UserFormType,
        description="Retrieves the user's submission for a specific form.",
    )

    @staticmethod
    def resolve_form(root, info: ResolveInfo) -> Optional[UserFormType]:
        user = info.context.user
        if not user.is_authenticated:
            return None

        # Get the latest form config/template (for dev purposes only)
        form_config = MRForm.objects.order_by("-created_at").first()

        if not form_config:
            return None

        evaluator = FormEvaluator(form_config, user)
        resolver = UserFormResolver(evaluator)

        return resolver.resolve()
