from django.db import transaction
from graphene import Field, List, Mutation, String

from form.types.UserFormType import UserFormType


class UpdateUserFormMutation(Mutation):
    class Arguments:
        input = UserFormInput(required=True)

    user_form = Field(UserFormType)
    errors = List(String)

    @classmethod
    def mutate(cls, root, info, input):
        try:
            with transaction.atomic():
                user_form = cls.save_project(input)
                return UpdateUserFormMutation(user_form=user_form, errors=[])

        except Exception as e:
            return UpdateUserFormMutation(user_form=None, errors=[str(e)])