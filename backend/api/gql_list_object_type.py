"""Custom implementation for DjangoObjectType which allows us to add
fields to Meta.
"""

from graphene_django import DjangoObjectType
from graphene_django.types import DjangoObjectTypeOptions


class GQLListObjectTypeOptions(DjangoObjectTypeOptions):
    search_fields = None


class GQLListObjectType(DjangoObjectType):
    class Meta:
        # Absolutely needed, otherwise Graphene will treat this as an
        # implementation and crash horribly
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(
        cls,
        search_fields=None,
        # Fields from base-class. Cannot be wrapped in a kwargs, sadly
        model=None,
        registry=None,
        skip_registry=False,
        only_fields=None,
        fields=None,
        exclude_fields=None,
        exclude=None,
        filter_fields=None,
        filterset_class=None,
        connection=None,
        connection_class=None,
        use_connection=None,
        interfaces=(),
        convert_choices_to_enum=True,
        _meta=None,
        **options,
    ):
        if not _meta:
            _meta = GQLListObjectTypeOptions(cls)

        _meta.search_fields = search_fields

        super().__init_subclass_with_meta__(
            model=model,
            registry=registry,
            skip_registry=skip_registry,
            only_fields=only_fields,
            fields=fields,
            exclude_fields=exclude_fields,
            exclude=exclude,
            filter_fields=filter_fields,
            filterset_class=filterset_class,
            connection=connection,
            connection_class=connection_class,
            use_connection=use_connection,
            interfaces=interfaces,
            convert_choices_to_enum=convert_choices_to_enum,
            _meta=_meta,
            **options,
        )
