from graphene import ObjectType, Field, ResolveInfo

from main.models import User
from main.types.UserType import UserType


class UserQueries(ObjectType):
    current_user = Field(
        UserType,
        description="Retrieves the user that is currently logged in.",
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
