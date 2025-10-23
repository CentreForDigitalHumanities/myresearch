from main.models import MRPermission
from research.models import Study
from research.types.StudyType import StudyType

from graphene import ID, Field, List, Mutation, ResolveInfo, String
from graphene_django.types import ErrorType


class UpdateStudyMutation(Mutation):

    study = Field(StudyType)
    errors = List(ErrorType)

    class Arguments:
        id = ID(required=True)
        title = String(required=True)

    @classmethod
    def mutate(
        cls,
        root: None,
        info: ResolveInfo,
        title: str,
        id: int,
    ):
        try:
            study = StudyType.get_queryset(Study.objects, info,).get(
                pk=id
            )
        except Study.DoesNotExist:
            error = ErrorType(
                field="id",
                messages=["Study not found."],
            )
            return cls(errors=[error])

        study.title = title

        study.save()
        return cls(study=study)
