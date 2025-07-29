from graphene import Schema, ObjectType

from main.queries import ListUsersQuery


class Query(ListUsersQuery, ObjectType):
    pass


schema = Schema(query=Query)
