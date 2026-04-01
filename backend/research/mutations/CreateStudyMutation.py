from research.other_models.reviews import StatusChange, SubmissionStatus
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
            # We first make a submission using the latest form
            latest_form = MRForm.objects.all().last()
            submission = UserFormSubmission.objects.create(
                user = user,
                form = latest_form,
            )
            submission.save()
            # Then create a study
            study = Study(created_by=user)
            study.save()
            # Create a StatusChange
            status_change = StatusChange.objects.create(
                status = SubmissionStatus.DRAFT,
                created_by = user,
                study = study
            )
            status_change.save()
            # link the study to the submission
            submission.study = study
            submission.save()
            return cls(study=study)
        else:
            error = ErrorType(
                field="", messages=["You are not authorized to create this study."]
            )
            return cls(errors=[error])
