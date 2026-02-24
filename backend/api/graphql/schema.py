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
from research.queries import StudyQuery
from main.queries import UserQueries

from form.mutations.UpdateUserFormSubmission import UpdateUserFormSubmission
from research.mutations.CreateStudyMutation import CreateStudyMutation
from research.mutations.UpdateStudyMutation import UpdateStudyMutation
from research.mutations.DeleteStudyMutation import DeleteStudyMutation


class Query(FormQueries, UserQueries, StudyQuery, ObjectType):
    pass


class Mutation(ObjectType):
    create_study = CreateStudyMutation.Field()
    update_study = UpdateStudyMutation.Field()
    delete_study = DeleteStudyMutation.Field()
    update_form_submission = UpdateUserFormSubmission.Field()


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
