from typing import Optional
from graphene import Field, List, NonNull, ObjectType, ResolveInfo

from django.db.models import QuerySet

from form.types.FormType import FormType
from form.models import Form


class FormQueries(ObjectType):
    form = Field(
        FormType, description="Retrieves the latest form. For testing purposes only."
    )

    @staticmethod
    def resolve_form(root, info: ResolveInfo) -> Optional[Form]:
        return (
            FormType.get_queryset(Form.objects, info)
            .order_by("-config__created_at")
            .first()
        )
