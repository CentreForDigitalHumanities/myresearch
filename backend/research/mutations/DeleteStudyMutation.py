from graphene import Mutation, ID, Boolean, ResolveInfo, List
from graphene_django.types import ErrorType

from research.types.StudyType import StudyType
from research.models.study import Study
from main.models import MRPermission


class DeleteStudyMutation(Mutation):

    ok = Boolean(required=True)
    errors = List(ErrorType)

    class Arguments:
        id = ID(required=True)

    @classmethod
    def mutate(
        cls,
        root: None,
        info: ResolveInfo,
        id: int,
    ):

        try:
            study = (
                StudyType.get_queryset(
                    Study.objects,
                    info,
                )
                .accessible_objects(info.context.user, MRPermission.DELETE)
                .get(pk=id)
            )
        except Study.DoesNotExist:
            error = ErrorType(
                field="id",
                messages=["Study not found."],
            )
            return cls(errors=[error], ok=False)

        # Soft delete if the study has ever been submitted.
        if study.has_been_submitted:
            study.is_deleted = True
            study.save()
        # Otherwise, do a regular (hard) delete.
        else:
            study.delete()

        return cls(ok=True)
