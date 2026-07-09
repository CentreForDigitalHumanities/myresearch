from graphene import Boolean, Field, ID, List, Mutation, ResolveInfo
from graphene_django.types import ErrorType

from main.models import MRPermission, User
from research.models.study import Study
from research.models.reviews import StatusChange, SubmissionStatus
from research.types.StudyType import StudyType


class CreateDraftStatusChange(Mutation):

    errors = List(ErrorType)
    ok = Boolean(required=True)

    class Arguments:
        study_id = ID(required=True)

    @classmethod
    def mutate(
        cls,
        root: None,
        info: ResolveInfo,
        study_id: int,
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
                ok=False,
                errors=[ErrorType(field="study_id", messages=["Study not found."])],
            )

        # Only allow privacy officers to return SUBMITTED studies back to DRAFT
        if not user.is_privacy_officer or study.status != SubmissionStatus.SUBMITTED:
            return cls(
                ok=False,
                errors=[
                    ErrorType(
                        field="status",
                        messages=["Not allowed to change status for this study."],
                    )
                ],
            )

        StatusChange.objects.create(
            status=SubmissionStatus.DRAFT,
            study=study,
            created_by=user,
        )

        return cls(ok=True)
