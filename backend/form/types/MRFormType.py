from graphene import ResolveInfo
from graphene_django import DjangoObjectType

from django.db.models import QuerySet

from form.types.StepType import StepType
from form.models import MRForm, Step


class MRFormType(DjangoObjectType):

    class Meta:
        model = MRForm
        fields = [
            "id",
            "name_nl",
            "name_en",
            "created_at",
            "updated_at",
            "steps",
        ]

    @classmethod
    def get_queryset(
        cls, queryset: QuerySet[MRForm], info: ResolveInfo
    ) -> QuerySet[MRForm]:
        return queryset

    @staticmethod
    def resolve_steps(parent: MRForm, info: ResolveInfo) -> QuerySet[Step]:
        return StepType.get_queryset(Step.objects, info).filter(form=parent)
