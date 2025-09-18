from graphene import ResolveInfo
from graphene_django import DjangoObjectType

from django.db.models import QuerySet

from form.models import SelectOption


class SelectOptionType(DjangoObjectType):
    class Meta:
        model = SelectOption
        fields = [
            "id",
            "label_nl",
            "label_en",
            "default_selected",
        ]

    @classmethod
    def get_queryset(
        cls, queryset: QuerySet[SelectOption], info: ResolveInfo
    ) -> QuerySet[SelectOption]:
        return queryset
