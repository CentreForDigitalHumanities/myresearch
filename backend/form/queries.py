from graphene import List, NonNull, ObjectType, ResolveInfo

from django.db.models import QuerySet

from form.types.FormType import FormType
from form.models import Form


class FormQueries(ObjectType):
    forms = List(NonNull(FormType), required=True)

    @staticmethod
    def resolve_forms(root, info: ResolveInfo) -> QuerySet[Form]:
        return FormType.get_queryset(Form.objects, info).all()
