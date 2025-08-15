from graphene import Schema, ObjectType

from form.types.QuestionType import (
    TrueFalseQuestionType,
    DateQuestionType,
    TextQuestionType,
    SelectQuestionType,
    FileUploadQuestionType,
    NumberQuestionType,
    BaseQuestionInterface,
)
from form.queries import FormQueries
from main.queries import ListUsersQuery


class Query(ListUsersQuery, FormQueries, ObjectType):
    pass


schema = Schema(
    query=Query,
    types=[
        BaseQuestionInterface,
        DateQuestionType,
        FileUploadQuestionType,
        NumberQuestionType,
        SelectQuestionType,
        TextQuestionType,
        TrueFalseQuestionType,
    ],
)
