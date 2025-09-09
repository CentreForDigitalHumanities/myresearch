from graphene import String, Mutation, Field, ID, Boolean, ResolveInfo

from main.types.UserType import UserType
from django.contrib.auth import get_user_model
    
class CreateUser(Mutation):
    class Arguments:
        username = String(required=True)
        email = String(required=True)

    user = Field(UserType)
    
    @classmethod
    def mutate(cls, root: None, info: ResolveInfo, username: str, email: str):
        user = get_user_model()(username=username, email=email)
        user.save()
        return CreateUser(user=user)


class UpdateUser(Mutation):
    class Arguments:
        id = ID(required=True)
        username = String(required=True)
        email = String(required=True)

    user = Field(UserType)

    @classmethod
    def mutate(cls, root: None, info: ResolveInfo, username: str, email: str):
        try:
            user = get_user_model().objects.get(pk=id)
        except get_user_model().DoesNotExist:
            raise Exception("user not found")

        if username is not None:
            user.username = username
        if email is not None:
            user.email = email

        user.save()
        return UpdateUser(user=user)


class DeleteUser(Mutation):
    class Arguments:
        id = ID(required=True)

    success = Boolean()

    @classmethod
    def mutate(cls, root: None, info: ResolveInfo, username: str, email: str):
        try:
            user = get_user_model().objects.get(pk=id)
        except user.DoesNotExist:
            raise Exception("User not found")

        user.delete()
        return DeleteUser(success=True)