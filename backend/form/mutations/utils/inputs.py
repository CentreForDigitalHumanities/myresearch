from graphene import InputObjectType, ID, List, NonNull, JSONString, Int


class ResponseInput(InputObjectType):
    id = ID()
    question_id = ID(required=True)
    answer = JSONString(required=True)
    repeat_index = Int()


class UserFormInput(InputObjectType):
    submission_id = ID(required=True)
    responses = List(NonNull(ResponseInput), required=True)
