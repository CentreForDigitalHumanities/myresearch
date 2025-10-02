from graphene import String, Mutation, Field, ID, Boolean, ResolveInfo, List
from graphene_django.types import ErrorType

from study.types.StudyType import StudyType
from study.models import Study
from main.models import MRPermissionTypes


class CreateStudy(Mutation):

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
        if not study.can_be_accessed_by(user, MRPermissionTypes.EDIT):
            error = ErrorType(
                field="", messages=["You are not authorized to create this study."]
            )
            return cls(errors=[error])

        # If permission check gets passed, save() and return the study
        study.save()
        return cls(study=study)


class UpdateStudy(Mutation):

    study = Field(StudyType)
    errors = List(ErrorType)

    class Arguments:
        id = ID(required=True)
        title = String(required=True)

    @classmethod
    def mutate(
        cls,
        root: None,
        info: ResolveInfo,
        title: str,
        id: int,
    ):

        study = Study.objects.get(pk=id)

        # Check if the study exists.
        if study is None:
            error = ErrorType(
                field="id",
                messages=["Study not found."],
            )
            return cls(errors=[error])

        user = info.context.user

        # Check if the user has Edit permission
        if not study.can_be_accessed_by(user, MRPermissionTypes.EDIT):
            error = ErrorType(
                field="", messages=["You are not authorized to update this study."]
            )
            return cls(errors=[error])

        # If the permission check has passed, update the title.
        study.title = title

        study.save()
        return cls(study=study)


class DeleteStudy(Mutation):

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

        study = Study.objects.get(pk=id)

        # Check if the study exists.
        if study is None:
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
