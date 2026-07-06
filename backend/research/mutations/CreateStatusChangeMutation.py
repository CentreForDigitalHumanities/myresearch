from graphene import Field, ID, List, Mutation, ResolveInfo, Argument
from graphene_django.types import ErrorType

from main.models import MRPermission, User
from research.models.study import Study
from research.models.reviews import StatusChange, SubmissionStatus
from research.types.StudyType import GQLSubmissionStatus, StudyType


class CreateStatusChange(Mutation):

    study = Field(StudyType)
    errors = List(ErrorType)

    class Arguments:
        study_id = ID(required=True)
        status = Argument(GQLSubmissionStatus, required=True)

    @classmethod
    def mutate(
        cls,
        root: None,
        info: ResolveInfo,
        study_id: int,
        status: SubmissionStatus,
    ):
        user: User = info.context.user

        try:
            study = (
                StudyType.get_queryset(Study.objects, info)
                .accessible_objects(user, MRPermission.VIEW)
                .get(pk=study_id)
            )
        except Study.DoesNotExist:
            return cls(
                errors=[ErrorType(field="study_id", messages=["Study not found."])]
            )

        StatusChange.objects.create(
            status=status,
            study=study,
            created_by=user,
        )

        return cls(study=study)
