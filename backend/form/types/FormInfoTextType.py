from graphene import ResolveInfo
from graphene_django import DjangoObjectType

from django.db.models import QuerySet

from form.models import FormInfoText


class FormInfoTextType(DjangoObjectType):
    class Meta:
        model = FormInfoText
        fields = [
            "id",
            "text_nl",
            "text_en",
        ]

    @classmethod
    def get_queryset(
        cls, queryset: QuerySet[FormInfoText], info: ResolveInfo
    ) -> QuerySet[FormInfoText]:
        return queryset
