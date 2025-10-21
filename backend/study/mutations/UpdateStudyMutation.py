from backend.main.models import MRPermission
from backend.study.models import Study
from backend.study.types.StudyType import StudyType


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
            study = StudyType.get_queryset(Study.objects, info).get(pk=id)
        except Study.DoesNotExist:
            error = ErrorType(
                field="id",
                messages=["Study not found."],
            )
            return cls(errors=[error])

        user = info.context.user

        # Check if the user has Edit permission
        if not study.can_be_accessed_by(user, MRPermission.EDIT):
            error = ErrorType(
                field="", messages=["You are not authorized to update this study."]
            )
            return cls(errors=[error])

        # If the permission check has passed, update the title.
        study.title = title

        study.save()
        return cls(study=study)
