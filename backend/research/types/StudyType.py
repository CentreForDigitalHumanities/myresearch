from django_filters import FilterSet, ModelMultipleChoiceFilter
from graphene import ResolveInfo

from django.db.models import QuerySet

from api.gql_list_object_type import GQLListObjectType
from main.models import User
from research.models import Study


class StudyFilter(FilterSet):

    created_by_ids = ModelMultipleChoiceFilter(
        field_name="created_by_id", queryset=User.objects.all()
    )


class StudyType(GQLListObjectType):
    class Meta:
        model = Study
        fields = [
            "id",
            "title",
            "created_by",
            "reference",
        ]
        filterset_class = StudyFilter
        search_fields = ["title", "reference"]

    @classmethod
    def get_queryset(
        cls,
        queryset: QuerySet[Study],
        info: ResolveInfo,
    ) -> QuerySet[Study]:
        return queryset
