from graphene import ResolveInfo
from graphene_django import DjangoObjectType

from django.db.models import QuerySet

from form.models import FormInfoQuestion


class FormInfoQuestionType(DjangoObjectType):
    class Meta:
        model = FormInfoQuestion
        fields = [
            "id",
            "text_nl",
            "text_en",
            "link",
        ]

    @classmethod
    def get_queryset(
        cls, queryset: QuerySet[FormInfoQuestion], info: ResolveInfo
    ) -> QuerySet[FormInfoQuestion]:
        return queryset
