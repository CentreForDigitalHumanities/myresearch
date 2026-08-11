from django.db.models import QuerySet
from graphene import (
    ID,
    Boolean,
    Field,
    Int,
    List,
    NonNull,
    ObjectType,
    ResolveInfo,
    String,
)

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
    is_overview = Boolean(required=True)

    questions = List(
        NonNull(BaseQuestionInterface),
        required=True,
    )
    substeps = List(
        lambda: NonNull(StepType),
        required=True,
    )
    step_info_text = List(
        NonNull(StepInfoTextType),
        required=False,
    )

    @staticmethod
    def resolve_step_info_text(
        parent, info: ResolveInfo
    ) -> QuerySet[StepInfoText] | None:
        if not parent.step_id:
            return None
        try:
            return StepInfoText.objects.filter(step_id=parent.step_id)
        except StepInfoText.DoesNotExist:
            return None
