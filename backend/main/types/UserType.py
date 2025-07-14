from graphene import ResolveInfo
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model

from django.db.models import QuerySet

from main.models import User


class UserType(DjangoObjectType):
    """
    NOTE: This Type was written during a very early phase of development as 
    a proof-of-concept for implementing graphql
    """
    class Meta:
        model = get_user_model()
        fields = ["username", "email"]

    @classmethod
    def get_queryset(cls, queryset: QuerySet[User], info: ResolveInfo) -> QuerySet[User]:
        return queryset.all()
