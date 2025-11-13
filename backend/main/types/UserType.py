from django.db.models import QuerySet
from graphene_django import DjangoObjectType
from graphene import ResolveInfo, String
from django.contrib.auth import get_user_model

from main.models import User


class UserType(DjangoObjectType):
    full_name = String(required=True)

    class Meta:
        model = get_user_model()
        fields = ["id", "username", "email", "first_name", "last_name", "is_staff"]

    @classmethod
    def get_queryset(
        cls, queryset: QuerySet[User], info: ResolveInfo
    ) -> QuerySet[User]:
        return queryset.all()

    @staticmethod
    def resolve_full_name(parent: User, info: ResolveInfo) -> str:
        return parent.get_full_name()
