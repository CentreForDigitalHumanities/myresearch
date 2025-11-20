import math
from collections import OrderedDict
from functools import partial

from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from graphene import Connection, Field, Int, List, NonNull, ObjectType, String
from graphene.relay.connection import ConnectionOptions
from graphene.types.argument import to_arguments
from graphene.utils.str_converters import to_snake_case
from graphene_django.filter.fields import convert_enum
from graphene_django.filter.utils import (
    get_filtering_args_from_filterset,
    get_filterset_class,
)
from graphene_django.utils import maybe_queryset
from promise import Promise

from api.graphql.search_filter import SearchFilter


class PaginationInfo(ObjectType):
    count = Int()
    limit = Int()
    offset = Int()


class PaginationConnection(Connection):
    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(cls, node=None, name=None, **options):
        _meta = ConnectionOptions(cls)
        base_name = node._meta.name

        if not name:
            name = "{}Connection".format(base_name)

        options["name"] = name
        _meta.node = node
        _meta.fields = OrderedDict(
            [
                (
                    "page_info",
                    Field(
                        PaginationInfo,
                        name="pageInfo",
                        required=True,
                        description="Pagination data for this connection.",
                    ),
                ),
                (
                    "results",
                    Field(
                        NonNull(List(node)),
                        description="Contains the nodes in this connection.",
                    ),
                ),
            ]
        )

        return super(Connection, cls).__init_subclass_with_meta__(
            _meta=_meta, **options
        )


class GQLListPaginationConnectionField(Field):
    """
    A custom implementation of Graphene's IterableConnectionField

    Also includes DjangoFilterConnectionField's django-filter integration.

    As for why we do not override ConnectionField? Well, that supports both
    cursor-based and offset based pagination. However, the latter is a very
    basic implementation.

    This implementation is offset only and incompatible with cursor offset
    paging, thus the full custom treatment.
    (We could override it, but then the cursor paging logic would still be
    present, polluting both the GraphQL schema and the code itself.)
    """

    def __init__(
        self,
        type_,
        fields=None,
        extra_filter_meta=None,
        filterset_class=None,
        search_enabled=True,
        *args,
        **kwargs,
    ):
        self.on = kwargs.pop("on", False)
        self._type = type_
        self._fields = fields
        self._provided_filterset_class = filterset_class
        self._filterset_class = None
        self._filtering_args = None
        self._extra_filter_meta = extra_filter_meta
        self._search_fields = []
        self._base_args = None

        kwargs.setdefault(
            "offset",
            Int(description="Offset in the list of results to start"),
        )
        kwargs.setdefault(
            "limit", Int(description="The number of items to retrieve")
        )
        kwargs.setdefault(
            "ordering", String(description="How the list should be ordered")
        )
        if search_enabled:
            kwargs.setdefault("search", String(description="Search query"))

        super().__init__(type_, *args, **kwargs)

    @classmethod
    def resolve_connection(cls, connection_type, *args, **kwargs):
        arguments = args[0]
        iterable = args[1]

        qs = maybe_queryset(iterable)

        if ordering := arguments.get("ordering"):
            ordering = to_snake_case(ordering)
            qs = qs.order_by(ordering)
        else:
            # Fallback option TODO: figure out a nice way to do this
            qs = qs.order_by("id")

        page_size = arguments.get("limit", 10)
        offset = arguments.get("offset", 1)

        assert isinstance(page_size, int), "Limit must be of type int"
        assert page_size > 0, "Limit must be positive integer greater than 0"

        paginator = Paginator(qs, page_size)
        page = paginator.get_page(math.floor(offset / page_size) + 1)

        connection = connection_type(
            results=page.object_list,
            page_info=PaginationInfo(
                limit=page_size,
                offset=offset,
                count=paginator.count,
            ),
        )
        connection.iterable = qs

        return connection

    @classmethod
    def connection_resolver(
        cls,
        resolver,
        connection,
        default_manager,
        queryset_resolver,
        root,
        info,
        **args,
    ):
        # eventually leads to DjangoObjectType's get_queryset (accepts queryset)
        # or a resolve_foo (does not accept queryset)
        iterable = resolver(root, info, **args)
        if iterable is None:
            iterable = default_manager
        # thus the iterable gets refiltered by resolve_queryset
        # but iterable might be promise
        iterable = queryset_resolver(connection, iterable, info, args)
        on_resolve = partial(cls.resolve_connection, connection, args)

        if Promise.is_thenable(iterable):
            return Promise.resolve(iterable).then(on_resolve)

        return on_resolve(iterable)

    @property
    def type(self):
        class NodeConnection(PaginationConnection):
            class Meta:
                node = self._type
                name = "{}NodeConnection".format(self._type._meta.name)

        return NodeConnection

    @classmethod
    def resolve_queryset(
        cls,
        connection,
        queryset,
        info,
        args,
        filtering_args,
        filterset_class,
        search_fields,
    ):
        """
        This method is almost fully copied over from Graphene-Django's DjangoFilterConnectionField.

        One notable omission is the following line:
        qs = super().resolve_queryset(connection, iterable, info, args)

        This causes queries to be executed multiple times and parameters passed to get_queryset() to be lost.
        """

        def filter_kwargs():
            kwargs = {}
            for k, v in args.items():
                if k in filtering_args:
                    if k == "order_by" and v is not None:
                        v = to_snake_case(v)
                    kwargs[k] = convert_enum(v)
            return kwargs

        if search_query := args.get("search"):
            queryset = SearchFilter(
                queryset, search_fields, search_query
            ).filter_queryset()

        filterset = filterset_class(
            data=filter_kwargs(), queryset=queryset, request=info.context
        )
        if filterset.is_valid():
            return filterset.qs
        raise ValidationError(filterset.form.errors.as_json())

    @property
    def search_fields(self):
        if not self._search_fields:
            self._search_fields = getattr(self.node_type._meta, "search_fields") or []
        return self._search_fields

    #
    # Below is stuff taken from graphene only
    #

    @property
    def node_type(self):
        return self.connection_type._meta.node

    @property
    def model(self):
        return self.node_type._meta.model

    def get_manager(self):
        if self.on:
            return getattr(self.model, self.on)
        else:
            return self.model._default_manager

    @property
    def args(self):
        return to_arguments(
            self._base_args or OrderedDict(), self.filtering_args
        )

    @args.setter
    def args(self, args):
        self._base_args = args

    @property
    def filterset_class(self):
        if not self._filterset_class:
            fields = (
                self.node_type._meta.filter_fields
                or self._fields
                or self.node_type._meta.fields.keys()
            )
            meta = {"model": self.model, "fields": fields}
            if self._extra_filter_meta:
                meta.update(self._extra_filter_meta)

            filterset_class = (
                self._provided_filterset_class
                or self.node_type._meta.filterset_class
            )
            self._filterset_class = get_filterset_class(filterset_class, **meta)

        return self._filterset_class

    @property
    def filtering_args(self):
        if not self._filtering_args:
            self._filtering_args = get_filtering_args_from_filterset(
                self.filterset_class, self.node_type
            )
        return self._filtering_args

    def get_queryset_resolver(self):
        return partial(
            self.resolve_queryset,
            filterset_class=self.filterset_class,
            filtering_args=self.filtering_args,
            search_fields=self.search_fields,
        )

    @property
    def connection_type(self):
        type = self.type
        if isinstance(type, NonNull):
            return type.of_type
        return type

    def wrap_resolve(self, parent_resolver):
        return partial(
            self.connection_resolver,
            parent_resolver,
            self.connection_type,
            self.get_manager(),
            self.get_queryset_resolver(),
        )
