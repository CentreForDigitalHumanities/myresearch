from research.models.reviews import SubmissionStatus
from main.models import MRPermission
from research.models.study import Study
from research.types.StudyType import StudyType

from graphene import ID, Boolean, Field, List, Mutation, ResolveInfo, String
from graphene_django.types import ErrorType


class UpdateStudySeenMutation(Mutation):
    study = Field(StudyType)
    ok = Boolean(required=True)
    errors = List(ErrorType)

    class Arguments:
        id = ID(required=True)
        is_seen = Boolean(required=True)

    @classmethod
    def mutate(
        cls,
        root: None,
        info: ResolveInfo,
        is_seen: bool,
        id: int,
    ):
        try:
            study = (
                StudyType.get_queryset(
                    Study.objects,
                    info,
                )
                .accessible_objects(info.context.user, MRPermission.VIEW)
                .get(pk=id)
            )
        except Study.DoesNotExist:
            error = ErrorType(
                field="id",
                messages=["Study not found."],
            )
            return cls(errors=[error], ok=False)

        if study.status == SubmissionStatus.DRAFT:
            error = ErrorType(
                field="id", messages=["Draft studies cannot be marked as seen."]
            )
            return cls(errors=[error], ok=False)

        study.is_seen = is_seen

        study.save()
        return cls(study=study, ok=True)
