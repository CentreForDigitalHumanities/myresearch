from backend.main.models import MRPermission
from backend.study.models import Study
from backend.study.types.StudyType import StudyType


from graphene import Field, List, Mutation, ResolveInfo, String
from graphene_django.types import ErrorType


class CreateStudyMutation(Mutation):

    study = Field(StudyType)
    errors = List(ErrorType)

    class Arguments:
        title = String(required=True)

    @classmethod
    def mutate(
        cls,
        root: None,
        info: ResolveInfo,
        title: str,
    ):

        user = info.context.user
        # Initialize the study, but do not save()
        study = Study(title=title, created_by=user)

        # Check if the user has Edit permission
        if not study.can_be_accessed_by(user, MRPermission.EDIT):
            error = ErrorType(
                field="", messages=["You are not authorized to create this study."]
            )
            return cls(errors=[error])

        # If permission check gets passed, save() and return the study
        study.save()
        return cls(study=study)
