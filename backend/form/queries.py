from typing import Optional
from graphene import Field, ObjectType, ResolveInfo


from form.types.MRFormType import MRFormType
from form.models import MRForm


class FormQueries(ObjectType):
    form = Field(
        MRFormType, description="Retrieves the latest form. For testing purposes only."
    )

    @staticmethod
    def resolve_form(root, info: ResolveInfo) -> Optional[MRForm]:
        return (
            MRFormType.get_queryset(MRForm.objects, info)
            .order_by("-config__created_at")
            .first()
        )
