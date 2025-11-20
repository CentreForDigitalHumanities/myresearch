import operator
from functools import reduce

from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django.db.models.constants import LOOKUP_SEP
from django.utils.text import smart_split, unescape_string_literal


def search_smart_split(search_terms):
    """generator that first splits string by spaces, leaving quoted phrases
    together, then it splits non-quoted phrases by commas.
    """
    for term in smart_split(search_terms):
        # trim commas to avoid bad matching for quoted phrases
        term = term.strip(",")
        if term.startswith(('"', "'")) and term[0] == term[-1]:
            # quoted phrases are kept togheter without any other split
            yield unescape_string_literal(term)
        else:
            # non-quoted tokens are split by comma, keeping only non-empty ones
            yield from (sub_term.strip() for sub_term in term.split(",") if sub_term)


class SearchFilter:
    """Advanced QS based searching, inspired by Django-admin and DRF
    SearchFilter (okay, mostly stolen from the latter)"""

    lookup_prefixes = {
        "^": "istartswith",
        "=": "iexact",
        "@": "search",
        "$": "iregex",
    }

    def __init__(self, queryset, search_fields, search_query):
        self._queryset = queryset
        self._search_fields = search_fields
        self._search_query = search_query

    def get_search_fields(self):
        return self._search_fields

    def get_search_terms(self):
        return self._search_query

    def construct_search(self, field_name, queryset):
        lookup = self.lookup_prefixes.get(field_name[0])
        if lookup:
            field_name = field_name[1:]
        else:
            # Use field_name if it includes a lookup.
            opts = queryset.model._meta
            lookup_fields = field_name.split(LOOKUP_SEP)
            # Go through the fields, following all relations.
            prev_field = None
            for path_part in lookup_fields:
                if path_part == "pk":
                    path_part = opts.pk.name
                try:
                    field = opts.get_field(path_part)
                except FieldDoesNotExist:
                    # Use valid query lookups.
                    if prev_field and prev_field.get_lookup(path_part):
                        return field_name
                else:
                    prev_field = field
                    if hasattr(field, "path_infos"):
                        # Update opts to follow the relation.
                        opts = field.path_infos[-1].to_opts
                    # django < 4.1
                    elif hasattr(field, "get_path_info"):
                        # Update opts to follow the relation.
                        opts = field.get_path_info()[-1].to_opts
            # Otherwise, use the field with icontains.
            lookup = "icontains"
        return LOOKUP_SEP.join([field_name, lookup])

    def must_call_distinct(self, queryset, search_fields):
        """
        Return True if 'distinct()' should be used to query the given lookups.
        """
        for search_field in search_fields:
            opts = queryset.model._meta
            if search_field[0] in self.lookup_prefixes:
                search_field = search_field[1:]
            # Annotated fields do not need to be distinct
            if (
                isinstance(queryset, models.QuerySet)
                and search_field in queryset.query.annotations
            ):
                continue
            parts = search_field.split(LOOKUP_SEP)
            for part in parts:
                field = opts.get_field(part)
                if hasattr(field, "get_path_info"):
                    # This field is a relation, update opts to follow the relation
                    path_info = field.get_path_info()
                    opts = path_info[-1].to_opts
                    if any(path.m2m for path in path_info):
                        # This field is a m2m relation so we know we need to call distinct
                        return True
                else:
                    # This field has a custom __ query transform but is not a relational field.
                    break
        return False

    def filter_queryset(self):
        if not self._search_fields or not self._search_query:
            return self._queryset

        orm_lookups = [
            self.construct_search(str(search_field), self._queryset)
            for search_field in self._search_fields
        ]

        base = self._queryset
        # generator which for each term builds the corresponding search
        conditions = (
            reduce(
                operator.or_,
                (models.Q(**{orm_lookup: term}) for orm_lookup in orm_lookups),
            )
            for term in search_smart_split(self._search_query)
        )
        queryset = self._queryset.filter(reduce(operator.and_, conditions))

        # Remove duplicates from results, if necessary
        if self.must_call_distinct(queryset, self._search_fields):
            # inspired by django.contrib.admin
            # this is more accurate than .distinct form M2M relationship
            # also is cross-database
            queryset = queryset.filter(pk=models.OuterRef("pk"))
            queryset = base.filter(models.Exists(queryset))
        return queryset
