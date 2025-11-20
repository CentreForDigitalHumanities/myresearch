from graphene import List, NonNull, ObjectType, Field, ResolveInfo

from main.models import User
from main.types.UserType import UserType


class UserQueries(ObjectType):
    current_user = Field(
        UserType,
        description="Retrieves the user that is currently logged in.",
    )

    users = List(
        NonNull(
            UserType
        ),
        required = True,
    )

    @staticmethod
    def resolve_current_user(root: None, info: ResolveInfo) -> User | None:
        user = info.context.user  # type: User
        if user.is_anonymous:
            return None
        try:
            return UserType.get_queryset(User.objects, info).get(id=user.pk)
        except User.DoesNotExist:
            # Should never happen.
            return None
        
    @staticmethod
    def resolve_users(root: None, info: ResolveInfo) -> list[User] | list:
        user = info.context.user  # type: User
        if user.is_anonymous:
            return []
        return UserType.get_queryset(User.objects, info).order_by("id")