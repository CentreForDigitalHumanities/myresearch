import graphene

from main.types.UserType import UserType
from django.contrib.auth import get_user_model
    
class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, username, email):
        user = get_user_model()(username=username, email=email)
        user.save()
        return CreateUser(user=user)


class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        username = graphene.String(required=True)
        email = graphene.String(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, id, username=None, email=None):
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


class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            user = get_user_model().objects.get(pk=id)
        except user.DoesNotExist:
            raise Exception("User not found")

        user.delete()
        return DeleteUser(success=True)