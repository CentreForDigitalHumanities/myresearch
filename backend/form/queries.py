from typing import Optional
from graphene import ID, Field, ObjectType, ResolveInfo, String


from main.models import User
from form.services.form_evaluator import FormEvaluator
from form.services.user_form_resolver import UserFormResolver
from form.types.UserFormType import UserFormType
from form.types.QuestionType import SelectQuestionType
from form.models import UserFormSubmission, SelectQuestion


class FormQueries(ObjectType):
    form = Field(
        UserFormType,
        submission_id=ID(required=True),
        mr_permission=String(required=True),
        description="Retrieves the user's submission for a specific form.",
    )

    @staticmethod
    def resolve_form(
        root,
        info: ResolveInfo,
        submission_id: str,
        mr_permission: str,
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


class QuestionQueries(ObjectType):

    select_question = Field(
        SelectQuestionType,
        id=ID(),
        annotation_key=String(),
        description="Retrieves a SelectQuestion by id or annotation_key, including its options.",
    )

    @staticmethod
    def resolve_select_question(
        root,
        info: ResolveInfo,
        id: str | None = None,
        annotation_key: str | None = None,
    ) -> Optional[SelectQuestionType]:
        user: User = info.context.user
        if not user.is_authenticated:
            return None

        if not id and not annotation_key:
            return None

        try:
            if id:
                question = SelectQuestion.objects.get(id=id)
            else:
                question = SelectQuestion.objects.get(annotation_key=annotation_key)

            return SelectQuestionType(question=question)
        except (SelectQuestion.DoesNotExist, AttributeError):
            return None
