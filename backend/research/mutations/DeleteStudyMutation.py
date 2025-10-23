from graphene import Mutation, ID, Boolean, ResolveInfo, List
from graphene_django.types import ErrorType
from django.db.models import QuerySet

from research.types.StudyType import StudyType
from research.models import Study
from main.models import MRPermission


class DeleteStudyMutation(Mutation):

    ok = Boolean()
    errors = List(ErrorType)

    class Arguments:
        id = ID(required=True)

    @classmethod
    def mutate(
        cls,
        root: None,
        info: ResolveInfo,
        id: int,
    ):

        try:
            study = StudyType.get_queryset(
                Study.objects,
                info,
            ).get(pk=id)
        except Study.DoesNotExist:
            error = ErrorType(
                field="id",
                messages=["Study not found."],
            )
            return cls(errors=[error])

        study.delete()
        return cls(ok=True)
