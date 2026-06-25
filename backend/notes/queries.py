from typing import Optional
from graphene import ID, Field, ObjectType, ResolveInfo
from notes.models import Note
from notes.types.NoteType import NoteType


class NoteQueries(ObjectType):
    note = Field(
        NoteType,
        slug=ID(required=True),
    )

    @staticmethod
    def resolve_note(root, info: ResolveInfo, slug: str) -> Optional[Note]:
        queryset = NoteType.get_queryset(
            Note.objects,
            info,
        )
        try:
            return queryset.get(slug=slug)
        except Note.DoesNotExist:
            return None
