<script
    lang="ts"
    setup
    generic="
        PageData extends GraphQLListData<UUListTypes.Data<string>>,
        TResult,
        Variables extends GraphQLListVariables
    "
>
import _ from "lodash";
import { UUList, type UUListTypes } from "cdh-vue-lib";
import type { UnwrapNestedRefs } from "vue";
import type {
    ApolloError,
    TypedDocumentNode,
    WatchQueryFetchPolicy,
} from "@apollo/client";
import { usePerformQuery } from "~/composables/usePerformQuery";
import type {
    GraphQLListData,
    GraphQLListVariables,
} from "~/components/shared/types";
import { useI18n } from "vue-i18n";
// This component has (mostly) been copied from DIAPP!
// See: https://github.com/CentreForDigitalHumanities/DIAPP
//
// Component defs
//
interface Props {
    queryDocument: TypedDocumentNode<TResult, Variables>;
    variables?: GraphQLListVariables;
    orderingOptions?: UUListTypes.SortOption[];
    dataMapper: (result: TResult) => PageData | null | undefined;
    container?: "default" | "sidebar";
    // Note: this will not determine if filters are enabled. It can be used to hide the filters through a button or such
    showFilters?: boolean;
    filters?: UUListTypes.FilterDefinition[];
    fetchPolicy?: WatchQueryFetchPolicy;
    pageSizeOptions?: number[];
}

const props = withDefaults(defineProps<Props>(), {
    variables: undefined,
    orderingOptions: undefined,
    container: "default",
    showFilters: true,
    filters: undefined,
    fetchPolicy: "cache-first",
    pageSizeOptions: () => [25, 50, 100],
});

const emits = defineEmits<{
    (
        e: "update:variables",
        value: UnwrapNestedRefs<GraphQLListVariables>,
    ): void;
    (e: "error", value: UnwrapNestedRefs<ApolloError>): void;
}>();

const { t } = useI18n();

// Constants
const DEFAULT_PAGE_SIZE = 50;
const DEFAULT_OFFSET = 0;

//
// Setup
//

// Create new variables object with sensible defaults
// It will be replaced by GraphQL with its own variables instance after the query
const initialVars = (function (): GraphQLListVariables {
    let vars: GraphQLListVariables;

    if (props.variables) {
        vars = _.cloneDeep(props.variables);
    } else {
        vars = {};
    }
    // Set defaults if omitted
    vars.limit = vars.limit ?? DEFAULT_PAGE_SIZE;
    vars.offset = vars.offset ?? DEFAULT_OFFSET;

    // Add any filter to variables, using initial values.
    if (props.filters) {
        props.filters.forEach((filter) => {
            if ("initial" in filter) {
                vars[filter.field] = filter.initial;
            }
        });
    }

    return vars;
})();

const { result, loading, variables } = usePerformQuery(
    {
        queryDocument: props.queryDocument,
        variables: initialVars,
        options: {
            fetchPolicy: props.fetchPolicy,
        },
    },
    (e) => {
        useNotification(t("List could not be fetched"), "danger");
        emits("error", e);
    },
);

watch(
    variables,
    (value) => {
        if (value === undefined) {
            emits("update:variables", initialVars);
            return;
        }
        emits("update:variables", value);
    },
    { immediate: true },
);

//
// Helpers
// Note: many helpers do not account for the feature not being supported by
// the query. However, this is guarded by being turned off in UUList using the
// xEnabled computed
//

// Data helper
// As the query returns data under a single, varying, key, we can't just use
// results directly. This shim solves that problem. TS is happy due to
// complicated typing :)
const pageData = computed<PageData | undefined>(() => {
    if (!result.value) {
        return undefined;
    }

    const data = props.dataMapper(result.value);
    if (data === null) {
        return undefined;
    }
    return data;
});

// Utility type to retrieve the actual type from the generic, and create one that's never null
type ItemType = NonNullable<PageData["results"][0]>;

const pageResults = computed<ItemType[] | undefined>(() => {
    if (pageData.value === undefined) {
        return undefined;
    }

    // This is a BS operation to force TS to realize null is not actually inside this array
    return _.chain(pageData.value.results).compact().value();
});

// Search helpers
const searchEnabled = computed(() => {
    if (variables.value === undefined) {
        return false;
    }

    return "search" in variables.value && variables.value.search !== undefined;
});
const searchQuery = computed(() => {
    return variables.value?.search ?? undefined;
});

function setSearchQuery(query: string) {
    if (variables.value === undefined) {
        return;
    }
    variables.value.search = query;
}

// Ordering helpers
const orderingEnabled = computed(() => {
    if (props.orderingOptions === undefined) {
        return false;
    }
    if (variables.value === undefined) {
        return false;
    }

    return (
        "ordering" in variables.value && variables.value.ordering !== undefined
    );
});
const currentOrdering = computed(() => {
    return variables.value?.ordering ?? undefined;
});

function setOrdering(ordering: string) {
    if (variables.value === undefined) {
        return;
    }
    variables.value.ordering = ordering;
}

// Page helpers
const currentPage = computed(() => {
    if (variables.value === undefined) {
        return 1;
    }

    // These values should never be undefined, but TS doesn't know that
    const offset = variables.value.offset ?? DEFAULT_OFFSET;
    const limit = variables.value.limit ?? DEFAULT_PAGE_SIZE;

    return Math.floor(offset / limit) + 1;
});

const currentPageSize = computed(() => {
    if (variables.value === undefined) {
        return DEFAULT_PAGE_SIZE;
    }
    return variables.value.limit ?? DEFAULT_PAGE_SIZE;
});

function switchPage(newPage: number) {
    if (variables.value === undefined) {
        return;
    }

    // This should never be undefined, but TS doesn't know that
    const limit = variables.value.limit ?? DEFAULT_PAGE_SIZE;

    variables.value.offset = (newPage - 1) * limit;
}

function switchPageSize(newPageSize: number) {
    if (variables.value === undefined) {
        return;
    }
    variables.value.offset = 0;
    variables.value.limit = newPageSize;
}

// Filter helpers
const filtersEnabled = computed(() => {
    if (!props.filters) {
        return false;
    }

    return props.showFilters || props.container === "sidebar";
});

const filterValues = computed(() => {
    if (props.filters === undefined || variables.value === undefined) {
        return undefined;
    }
    const values: UUListTypes.FilterValues = {};

    for (const filter of props.filters) {
        values[filter.field] = variables.value[
            filter.field
        ] as UUListTypes.FilterValue;
    }

    return values;
});

function updateFilterValues(newFilterValues: UUListTypes.FilterValues) {
    if (props.filters === undefined || variables.value === undefined) {
        return undefined;
    }

    for (const [key, value] of Object.entries(newFilterValues)) {
        if (variables.value[key] !== value) {
            (variables.value as Record<string, UUListTypes.FilterValue>)[key] =
                value;
        }
    }
}
</script>

<template>
    <UUList
        :container="container"
        :is-loading="loading"
        :search-enabled="searchEnabled"
        :search="searchQuery"
        :page-size="currentPageSize"
        :current-page="currentPage"
        :page-size-options="pageSizeOptions"
        :filters-enabled="filtersEnabled"
        :filters="filters"
        :filter-values="filterValues"
        :sort-enabled="orderingEnabled"
        :sort-options="orderingOptions"
        :current-sort="currentOrdering"
        :total-data="pageData?.pageInfo?.count ?? 0"
        :data="pageResults"
        @update:current-page="(value: number) => switchPage(value)"
        @update:page-size="(value: number) => switchPageSize(value)"
        @update:search="(value: string) => setSearchQuery(value)"
        @update:filter-values="
            (value: UUListTypes.FilterValues) => updateFilterValues(value)
        "
        @update:current-sort="(value: string) => setOrdering(value)"
    >
        <template #data="{ data, isLoading }">
            <slot
                name="data"
                :data="data as ItemType[]"
                :is-loading="isLoading"
            />
        </template>
        <template #filters-top="{ data, isLoading }">
            <slot
                name="filters-top"
                :data="data as ItemType[]"
                :is-loading="isLoading"
            />
        </template>
        <template #filters-bottom="{ data, isLoading }">
            <slot
                name="filters-bottom"
                :data="data as ItemType[]"
                :is-loading="isLoading"
            />
        </template>
    </UUList>
</template>
