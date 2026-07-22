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

from form.models import StepInfo
from form.types.StepInfoType import StepInfoType
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
    step_info = List(
        NonNull(StepInfoType),
        required=False,
    )

    @staticmethod
    def resolve_step_info(parent, info: ResolveInfo) -> QuerySet[StepInfo] | None:
        if not parent.step_id:
            return None
        try:
            return StepInfo.objects.filter(step_id=parent.step_id)
        except StepInfo.DoesNotExist:
            return None
