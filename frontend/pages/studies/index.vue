<script lang="ts" setup>
import { graphql } from "~/generated/gql";
import type { GraphQLListVariables } from "~/components/shared/types";
import { SharedGraphQLList } from "#components";
import { useI18n } from "vue-i18n";
import type { UUListTypes } from "cdh-vue-lib";
import { useQuery } from "@vue/apollo-composable";
import type { GetUsersQuery } from "~/generated/gql/graphql"

const { t } = useI18n();

// The query supplying the data for the list
const GET_STUDY_PAGES = graphql(`
query GetStudyPages(
  $limit: Int
  $offset: Int
  $ordering: String
  $search: String
  $createdByIds: [ID]
) {
  studyPages(
    mrPermission: "View"
    limit: $limit
    offset: $offset
    ordering: $ordering
    search: $search
    createdByIds: $createdByIds
  ) {
    results {
      id
      title
      createdBy {
        id
        fullName
      }
    }
    pageInfo {
      count
      limit
      offset
    }
  }
}
`);

const variables = ref<GraphQLListVariables>({
    search: "",
    ordering: "title",
    createdByIds: [], 
});

const orderingOptions = computed(() => {
    return [
        {
            field: "title",
            label: t("title ascending"),
        },
        {
            field: "-title",
            label: t("title descending"),
        },
        {
            field: "createdBy__last_name",
            label: t("last name ascending"),
        },
        {
            field: "-createdBy__last_name",
            label: t("last name descending"),
        },
    ];
});

// Secondary Query to derive filter options from
const GET_USERS = graphql(`
query getUsers {
  users {
    id
    fullName
  }
}
`)


const { result } = useQuery<GetUsersQuery>(GET_USERS);

const users = computed(() => result.value?.users ?? []);

const filters = computed<UUListTypes.FilterDefinition[]>(() => {
    const userFilter: UUListTypes.FilterDefinition = {
        field: "createdByIds",
        label: t("Creator"),
        options: users.value.map((user: any) => [
            user.id,
            user.fullName,
        ]),
        type: "checkbox",
        initial: [],
    };
    return [userFilter];
});

</script>

<template>
    <SharedGraphQLList
        v-model:variables="variables"
        :query-document="GET_STUDY_PAGES"
        :data-mapper="(result: any) => result?.studyPages ?? undefined"
        :ordering-options="orderingOptions"
        :filters="filters"
        fetch-policy="no-cache"
    >
        <template #data="{ data, isLoading }">
            <table class="table table-hover table-striped">
                <thead>
                    <tr>
                        <th>
                            {{ $t("Title") }}
                        </th>
                        <th>
                            {{ $t("Creator") }}
                        </th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="row in data" :key="row.id">
                        <td class="align-middle">
                            {{ row.title }}
                        </td>
                        <td>
                            {{ row.createdBy.fullName }}
                        </td>
                    </tr>
                    <tr v-if="isLoading">
                        <td colspan="5" class="text-center">
                            <Loading />
                        </td>
                    </tr>
                    <tr v-if="!isLoading && data?.length === 0">
                        <td colspan="5" class="text-center">
                            {{ $t("errors.no_results_found") }}
                        </td>
                    </tr>
                </tbody>
            </table>
        </template>
    </SharedGraphQLList>
</template>
