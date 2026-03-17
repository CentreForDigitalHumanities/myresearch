from graphene import ID, Field, Int, List, NonNull, ObjectType, ResolveInfo, String

from django.db.models import QuerySet

from form.models import StepInfoText
from form.types.StepInfoTextType import StepInfoTextType
from form.types.QuestionType import BaseQuestionInterface


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
    info_text = Field(StepInfoTextType)

    @staticmethod
    def resolve_info_text(parent, info: ResolveInfo) -> StepInfoText:
        if not parent.step_id:
            return StepInfoText.objects.none()
        return StepInfoText.objects.get(step_id=parent.step_id)
