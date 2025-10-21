from graphene import Mutation, ID, Boolean, ResolveInfo, List
from graphene_django.types import ErrorType

from study.models import Study
from main.models import MRPermissionTypes


class DeleteStudyMutation(Mutation):

    ok = Boolean()
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

        user = info.context.user

        try:
            study = Study.objects.get(pk=id)
        except Study.DoesNotExist:
            error = ErrorType(
                field="id",
                messages=["Study not found."],
            )
            return cls(errors=[error])

        # Check if the user has Edit permission
        if not study.can_be_accessed_by(user, MRPermissionTypes.EDIT):
            error = ErrorType(
                field="", messages=["You are not authorized to delete this study."]
            )
            return cls(errors=[error])

        study.delete()
        return cls(ok=True)
