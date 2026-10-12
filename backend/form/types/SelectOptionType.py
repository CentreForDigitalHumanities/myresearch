from graphene import Boolean, ResolveInfo
from graphene_django import DjangoObjectType

from django.db.models import QuerySet

from form.models import SelectOption


class SelectOptionType(DjangoObjectType):
    default_selected = Boolean(required=True)

    class Meta:
        model = SelectOption
        fields = [
            "id",
            "label_nl",
            "label_en",
        ]

    @classmethod
    def get_queryset(
        cls, queryset: QuerySet[SelectOption], info: ResolveInfo
    ) -> QuerySet[SelectOption]:
        return queryset

    @staticmethod
    def resolve_default_selected(parent, info: ResolveInfo) -> bool:
        return parent.default_selected
