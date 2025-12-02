from graphene import ID, Int, List, NonNull, ObjectType, ResolveInfo, String

from django.db.models import QuerySet

from form.models import StepInfoQuestion, StepInfoText
from form.types.StepInfoTextType import StepInfoTextType
from form.types.QuestionType import BaseQuestionInterface
from form.types.StepInfoQuestionType import StepInfoQuestionType


class StepType(ObjectType):
    """Represents a single instance of a step for a user (accounting for repeats)."""

    step_id = ID(required=True)
    name_nl = String(required=True)
    name_en = String(required=True)
    description_nl = String()
    description_en = String()
    slug = String(required=True)
    repeat_index = Int(required=True)

    questions = List(
        NonNull(BaseQuestionInterface),
        required=True,
    )
    substeps = List(
        lambda: NonNull(StepType),
        required=True,
    )
    info_questions = List(NonNull(StepInfoQuestionType), required=True)
    info_texts = List(NonNull(StepInfoTextType), required=True)

    @staticmethod
    def resolve_info_questions(parent, info: ResolveInfo) -> QuerySet[StepInfoQuestion]:
        if not parent.step_id:
            return StepInfoQuestion.objects.none()
        return StepInfoQuestion.objects.filter(step_id=parent.step_id)

    @staticmethod
    def resolve_info_texts(parent, info: ResolveInfo) -> QuerySet[StepInfoText]:
        if not parent.step_id:
            return StepInfoText.objects.none()
        return StepInfoText.objects.filter(step_id=parent.step_id)
