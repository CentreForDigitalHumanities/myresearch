from graphene import ResolveInfo
from graphene_django import DjangoObjectType

from django.db.models import QuerySet

from form.models import FormConfig


class FormConfigType(DjangoObjectType):

    class Meta:
        model = FormConfig
        fields = [
            "id",
            "name",
            "version",
            "created_at",
            "updated_at",
            "form",
        ]

    @classmethod
    def get_queryset(
        cls, queryset: QuerySet[FormConfig], info: ResolveInfo
    ) -> QuerySet[FormConfig]:
        return queryset
