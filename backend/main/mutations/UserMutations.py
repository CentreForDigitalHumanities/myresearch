from graphene import String, Mutation, Field, ID, Boolean, ResolveInfo, List
from graphene_django.types import ErrorType

from main.types.UserType import UserType
from django.contrib.auth import get_user_model
    
class CreateUser(Mutation):

    user = Field(UserType)

    class Arguments:
        username = String(required=True)
        email = String(required=True)
    
    @classmethod
    def mutate(cls, root: None, info: ResolveInfo, username: str, email: str):
        user = get_user_model()(username=username, email=email)
        user.save()
        return cls(user=user)


class UpdateUser(Mutation):

    user = Field(UserType)
    errors = List(ErrorType)

    class Arguments:
        id = ID(required=True)
        username = String(required=True)
        email = String(required=True)

    @classmethod
    def mutate(cls, root: None, info: ResolveInfo, username: str, email: str):

        user = get_user_model().objects.get(pk=id)
        
        if user is None:
            error = ErrorType(
                field="id",
                messages=["User not found."],
            )
            return cls(errors=[error])

        if username is not None:
            user.username = username
        if email is not None:
            user.email = email

        user.save()
        return cls(user=user)


class DeleteUser(Mutation):

    ok = Boolean()
    errors = List(ErrorType)

    class Arguments:
        id = ID(required=True)

    @classmethod
    def mutate(cls, root: None, info: ResolveInfo, username: str, email: str):
        user = get_user_model().objects.get(pk=id)
        
        if user is None:
            error = ErrorType(
                field="id",
                messages=["User not found."],
            )
            return cls(ok=False, errors=[error])

        user.delete()
        return cls(ok=True)