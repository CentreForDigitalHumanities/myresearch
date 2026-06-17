from main.models import User
from research.models.study import Study
from research.types.StudyType import StudyType
from research.services.create_study import create_study

from graphene import Field, List, Mutation, ResolveInfo
from graphene_django.types import ErrorType


class CreateStudyMutation(Mutation):

    study = Field(StudyType)
    errors = List(ErrorType)

    @classmethod
    def mutate(
        cls,
        root: None,
        info: ResolveInfo,
    ):

        user: User = info.context.user

        # Check if the user has Create permission
        if Study.can_be_created_by(user):
            study = create_study(user)
            return cls(study=study)
        else:
            error = ErrorType(
                field="", messages=["You are not authorized to create this study."]
            )
            return cls(errors=[error])
