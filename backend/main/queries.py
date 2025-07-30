import graphene

from graphene_django import DjangoListField

from main.types.UserType import UserType
from django.contrib.auth import get_user_model


class ListUsersQuery(graphene.ObjectType):
    users = DjangoListField(UserType)

    def resolve_users(self, info):
        return UserType.get_queryset(get_user_model().objects.all(), info)
