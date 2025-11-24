from typing import Optional
from graphene import ID, Field, ObjectType, ResolveInfo


from form.services.form_evaluator import FormEvaluator
from form.types.UserFormType import UserFormResolver, UserFormType
from form.types.MRFormType import MRFormType
from form.models import MRForm, Step


class FormQueries(ObjectType):
    form = Field(
        MRFormType,
        description="Retrieves the latest top-level form. For testing purposes only.",
    )

    user_form = Field(
        UserFormType,
        description="Retrieves the user's submission for a specific form.",
    )

    @staticmethod
    def resolve_form(root, info: ResolveInfo) -> Optional[MRForm]:
        return (
            MRFormType.get_queryset(MRForm.objects, info)
            .order_by("-created_at")
            .first()
        )

    @staticmethod
    def resolve_user_form(root, info: ResolveInfo) -> Optional[UserFormType]:
        user = info.context.user
        if not user.is_authenticated:
            return None

        # Get the latest form template
        form = MRForm.objects.order_by("-created_at").first()

        if not form:
            return None

        evaluator = FormEvaluator(form, user)
        submission = evaluator.submission

        resolver = UserFormResolver(evaluator)
        steps = resolver.resolve_steps()

        return UserFormType(
            form_id=form.pk,
            name=form.name,
            steps=steps,
            submission_id=submission.pk if submission else None,
            started_at=submission.started_at if submission else None,
            completed_at=submission.completed_at if submission else None,
        )
