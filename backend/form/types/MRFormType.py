from typing import Optional
from graphene import ResolveInfo
from graphene_django import DjangoObjectType

from django.db.models import QuerySet

from form.types.StepType import StepType
from backend.form.types.MRFormConfigType import MRFormConfigType
from form.models import MRForm, MRFormConfig, Step


class MRFormType(DjangoObjectType):

    class Meta:
        model = MRForm
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
        cls, queryset: QuerySet[MRForm], info: ResolveInfo
    ) -> QuerySet[MRForm]:
        return queryset

    @staticmethod
    def resolve_config(parent: MRForm, info: ResolveInfo) -> Optional[MRFormConfig]:
        try:
            return MRFormConfigType.get_queryset(MRFormConfig.objects, info).get(
                form=parent
            )
        except MRFormConfig.DoesNotExist:
            return None

    @staticmethod
    def resolve_steps(parent: MRForm, info: ResolveInfo) -> QuerySet[Step]:
        return (
            StepType.get_queryset(Step.objects, info)
            .filter(form=parent)
            .order_by("form_order")
        )
