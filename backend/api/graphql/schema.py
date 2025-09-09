from graphene import Schema, ObjectType

from form.types.QuestionType import (
    QuestionType,
    BaseQuestionInterface,
    TrueFalseQuestionType,
    DateQuestionType,
    TextQuestionType,
    SelectQuestionType,
    FileUploadQuestionType,
    NumberQuestionType,
)
from form.queries import FormQueries
from main.queries import ListUsersQuery


class Query(ListUsersQuery, FormQueries, ObjectType):
    pass


schema = Schema(
    query=Query,
    types=[
        # These types are not queried directly, so they are included here to
        # make Graphene aware of them.
        QuestionType,
        BaseQuestionInterface,
        TrueFalseQuestionType,
        DateQuestionType,
        TextQuestionType,
        SelectQuestionType,
        FileUploadQuestionType,
        NumberQuestionType,
    ],
)
