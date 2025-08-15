from typing import Optional
from graphene import ResolveInfo
from graphene_django import DjangoObjectType

from django.db.models import QuerySet

from form.types.StepType import StepType
from form.types.FormConfigType import FormConfigType
from form.models import Form, FormConfig, Step


class FormType(DjangoObjectType):

    class Meta:
        model = Form
        fields = [
            "id",
            "name_nl",
            "name_en",
            "description_nl",
            "description_en",
            "config",
            "steps",
        ]

    @classmethod
    def get_queryset(
        cls, queryset: QuerySet[Form], info: ResolveInfo
    ) -> QuerySet[Form]:
        return queryset

    @staticmethod
    def resolve_config(parent: Form, info: ResolveInfo) -> Optional[FormConfig]:
        try:
            return FormConfigType.get_queryset(FormConfig.objects, info).get(
                form=parent
            )
        except FormConfig.DoesNotExist:
            return None

    @staticmethod
    def resolve_steps(parent: Form, info: ResolveInfo) -> QuerySet[Step]:
        return (
            StepType.get_queryset(Step.objects, info)
            .filter(form=parent)
            .order_by("form_order")
        )
