from research.models import Study
from research.types.StudyType import StudyType

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

        # Check if the user has Create permission
        if Study.can_be_created_by(user):
            study = Study(title=title, created_by=user)
            study.save()
            return cls(study=study)
        else:
            error = ErrorType(
                field="", messages=["You are not authorized to create this study."]
            )
            return cls(errors=[error])
