from graphene import Schema, ObjectType

from main.queries import ListUsersQuery
from main.mutations.UserMutations import (
    CreateUser,
    UpdateUser,
    DeleteUser,
)

class Query(ListUsersQuery, ObjectType):
    pass

class Mutation(ObjectType):

    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()


schema = Schema(
    query=Query,
    mutation=Mutation,
)
