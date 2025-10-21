from graphene import ResolveInfo
from graphene_django import DjangoObjectType

from django.db.models import QuerySet

from study.models import Study
from main.models import User, MRPermission


class StudyType(DjangoObjectType):
    class Meta:
        model = Study
        fields = [
            "id",
            "title",
            "created_by",
        ]

    @classmethod
    def get_queryset(
        cls,
        queryset: QuerySet[Study],
        info: ResolveInfo,
        permission: int,
    ) -> QuerySet[Study]:
        """
        Return the queryset of studies, based on the permission, defined in the
        query.

        TODO: This function should probably live in some kind of mixin for all
        DjangoObjectTypes in MyResearch.
        """

        user = info.context.user

        if not user.is_authenticated:
            return queryset.none()
        if permission == MRPermission.VIEW:
            return cls.viewable_queryset(user, queryset)
        if permission == MRPermission.EDIT:
            return cls.editable_queryset(user, queryset)
        # NOTE: This should never happen.
        raise ValueError(
            f"{cls}.get_queryset() has received a permission type which has not "
            "yet been implemented."
        )

    @classmethod
    def viewable_queryset(
        cls, user: User, queryset: QuerySet[Study]
    ) -> QuerySet[Study]:
        """
        Filter the queryset based on view-permissions
        """
        if user.is_privacy_officer or user.is_fetc_member:
            return queryset
        return queryset.filter(created_by=user)

    @classmethod
    def editable_queryset(
        cls, user: User, queryset: QuerySet[Study]
    ) -> QuerySet[Study]:
        """
        Filter the queryset based on edit-permissions
        """
        return queryset.filter(created_by=user)
