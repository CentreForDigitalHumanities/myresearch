from graphene import Schema, ObjectType

from form.types import StepType
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
from study.queries import StudyQuery

from study.mutations.CreateStudyMutation import CreateStudyMutation
from study.mutations.UpdateStudyMutation import UpdateStudyMutation
from study.mutations.DeleteStudyMutation import DeleteStudyMutation


class Query(ListUsersQuery, FormQueries, StudyQuery, ObjectType):
    pass


class Mutation(ObjectType):

    create_study = CreateStudyMutation.Field()
    update_study = UpdateStudyMutation.Field()
    delete_study = DeleteStudyMutation.Field()


schema = Schema(
    query=Query,
    mutation=Mutation,
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
