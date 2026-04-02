from graphene import ID, ObjectType, String, List, DateTime, NonNull

from form.types.StepType import StepType


class UserFormType(ObjectType):
    """The form structure as it appears to a specific user."""

    form_id = ID(required=True)
    name_nl = String(required=True)
    name_en = String(required=True)
    steps = List(
        NonNull(StepType),
        required=True,
    )
    submission_id = ID(required=True)
    started_at = DateTime()
    completed_at = DateTime()
