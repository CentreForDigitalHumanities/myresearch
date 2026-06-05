from django.db.models import QuerySet
from graphene import (
    ResolveInfo,
)
from graphene_django import DjangoObjectType
from notes.models import Note


class NoteType(DjangoObjectType):
    class Meta:
        model = Note
        fields = [
            "pk",
            "slug",
            "title",
            "content",
        ]

    @classmethod
    def get_queryset(
        cls, queryset: QuerySet[Note], info: ResolveInfo
    ) -> QuerySet[Note]:
        return queryset
