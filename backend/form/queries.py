from typing import Optional
from graphene import ID, Field, ObjectType, ResolveInfo, String, List, Int


from main.models import User
from form.services.form_evaluator import FormEvaluator
from form.services.user_form_resolver import UserFormResolver
from form.types.UserFormType import UserFormType
from form.types.QuestionType import SelectQuestionType
from form.types.StepType import StepType
from form.models import UserFormSubmission, SelectQuestion, RepeatableStep, RepeatIndex
from form.models.responses import QuestionResponse


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
        form_id=ID(),
        description="Retrieves a SelectQuestion by id or annotation_key, including its options.",
    )

    @staticmethod
    def resolve_select_question(
        root,
        info: ResolveInfo,
        form_id: str | None = None,
        id: str | None = None,
        annotation_key: str | None = None,
    ) -> Optional[SelectQuestionType]:
        user: User = info.context.user
        if not user.is_authenticated:
            return None

        if not id and not (annotation_key and form_id):
            return None

        try:
            if id:
                question = SelectQuestion.objects.get(
                    id=id,
                )
            else:
                question = SelectQuestion.objects.get(
                    annotation_key=annotation_key, form_id=form_id
                )

            return SelectQuestionType(question=question)
        except SelectQuestion.DoesNotExist:
            return None


class RepeatableStepQueries(ObjectType):

    repeatable_steps_with_repeats = Field(
        List(StepType),
        repeatable_id=ID(required=True),
        response_id=ID(required=False),
        description="Retrieves a RepeatableStep for each repeat index in the response's answer, with the repeat_index field populated.",
    )

    @staticmethod
    def resolve_repeatable_steps_with_repeats(
        root,
        info: ResolveInfo,
        repeatable_id: str,
        response_id: str = None,
    ) -> list[StepType]:
        user: User = info.context.user
        if not user.is_authenticated:
            return []

        if not response_id:
            return []

        try:
            repeatable_step = RepeatableStep.objects.get(pk=repeatable_id)
            question_response = QuestionResponse.objects.get(pk=response_id)

            # Extract repeat indices from the answer
            answer = question_response.answer
            repeat_indices = answer.get("value", []) if isinstance(answer, dict) else []

            # Fetch the repeat index objects
            repeat_index_objects = RepeatIndex.objects.filter(pk__in=repeat_indices)

            return [
                StepType(
                    step_id=repeatable_step.id,
                    name_nl=repeatable_step.name,
                    name_en=repeatable_step.name,
                    description_nl=repeatable_step.description,
                    description_en=repeatable_step.description,
                    slug=repeatable_step.slug,
                    is_overview=repeatable_step.is_overview,
                    questions=[],
                    substeps=[],
                    background=None,
                    repeat_index=int(repeat_idx.id),
                )
                for repeat_idx in repeat_index_objects
            ]
        except (RepeatableStep.DoesNotExist, QuestionResponse.DoesNotExist):
            return []
