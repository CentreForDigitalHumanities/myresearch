from graphene import Schema, ObjectType

from research.types.StudyType import GQLSubmissionStatus
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
from form.queries import FormQueries, QuestionQueries
from research.queries import StudyQuery
from main.queries import UserQueries
from notes.queries import NoteQueries

from form.mutations.CreateUserFormRevision import CreateUserFormRevision
from form.mutations.UpdateUserFormSubmission import UpdateUserFormSubmission
from form.mutations.repeat_mutations import CreateRepeatMutation, DeleteRepeatMutation
from research.mutations.CreateStudyMutation import CreateStudyMutation
from research.mutations.UpdateStudyMutation import UpdateStudyMutation
from research.mutations.DeleteStudyMutation import DeleteStudyMutation


class Query(FormQueries, UserQueries, StudyQuery, QuestionQueries, NoteQueries, ObjectType):
    pass


class Mutation(ObjectType):
    create_study = CreateStudyMutation.Field()
    update_study = UpdateStudyMutation.Field()
    delete_study = DeleteStudyMutation.Field()
    update_form_submission = UpdateUserFormSubmission.Field()
    create_user_form_revision = CreateUserFormRevision.Field()
    create_repeat = CreateRepeatMutation.Field()
    delete_repeat = DeleteRepeatMutation.Field()


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
