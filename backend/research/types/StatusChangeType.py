from graphene import Enum, Field
from graphene_django import DjangoObjectType
from research.models.reviews import StatusChange, SubmissionStatus

GQLSubmissionStatus = Enum.from_enum(SubmissionStatus)


class StatusChangeType(DjangoObjectType):
    status = Field(GQLSubmissionStatus, required=True)

    class Meta:
        model = StatusChange
        fields = ["id", "status", "created_by", "created_at"]
