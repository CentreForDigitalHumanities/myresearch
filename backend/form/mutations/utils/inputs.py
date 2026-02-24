from graphene import Boolean, InputObjectType, ID, List, NonNull, JSONString, Int


class ResponseInput(InputObjectType):
    id = ID()
    question_id = ID(required=True)
    answer = JSONString(required=True)
    repeat_index = Int(required=True)


class UserFormInput(InputObjectType):
    submission_id = ID()
    form_config_id = ID()
    responses = List(NonNull(ResponseInput), required=True)
    create_study = Boolean(required=False, default_value=False)
