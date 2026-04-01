from form.models import MRForm, UserFormSubmission
from main.models import User
from research.models import Study
from research.types.StudyType import StudyType

from graphene import ID, Field, List, Mutation, ResolveInfo, String
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
            study = Study(created_by=user)
            study.save()
            # We make a submission using the latest form
            latest_form = MRForm.objects.last()
            submission = UserFormSubmission.objects.create(
                user = user,
                form = latest_form,
                study = study,
            )
            submission.save()
            return cls(study=study)
        else:
            error = ErrorType(
                field="", messages=["You are not authorized to create this study."]
            )
            return cls(errors=[error])
