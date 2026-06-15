<script lang="ts" setup>
import { graphql } from "~/generated/gql";
import type { GraphQLListVariables } from "~/components/shared/types";
import { SharedGraphQLList } from "#components";
import { useI18n } from "vue-i18n";
import type { UUListTypes } from "cdh-vue-lib";
import Loading from "~/components/shared/Loading.vue";
import { useQuery } from "@vue/apollo-composable";
import { SubmissionStatus } from "~/generated/gql/graphql";
import type { GetFacultyQuestionQuery } from "~/generated/gql/graphql";
import { useTranslatedStatus } from "~/composables/useTranslatedStatus";

const { t } = useI18n();

// The query supplying the data for the list
const GET_STUDY_PAGES = graphql(`
    query GetStudyPages(
        $limit: Int
        $offset: Int
        $ordering: String
        $search: String
        $statuses: [String]
        $faculties: [ID]
    ) {
        studyPages(
            mrPermission: "View"
            limit: $limit
            offset: $offset
            ordering: $ordering
            search: $search
            statuses: $statuses
            faculties: $faculties
        ) {
            results {
                id
                title
                reference
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
    ordering: "-reference",
    statuses: [],
    faculties: [],
});

const orderingOptions = computed(() => {
    return [
        {
            field: "reference",
            label: t("Ref. number ascending"),
        },
        {
            field: "-reference",
            label: t("Ref. number descending"),
        },
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

const GET_FACULTY_QUESTION = graphql(`
    query GetFacultyQuestion {
        selectQuestion(annotationKey: "faculty", formId: 1) {
            options {
                id
                labelEn
                labelNl
            }
        }
    }
`);

const { result: facultyResult, loading: facultyLoading } =
    useQuery<GetFacultyQuestionQuery>(GET_FACULTY_QUESTION);

const facultyOptions = computed(
    () => facultyResult.value?.selectQuestion?.options ?? [],
);

const filters = computed<UUListTypes.FilterDefinition[]>(() => {
    const statusFilter: UUListTypes.FilterDefinition = {
        field: "statuses",
        label: t("Status"),
        options: Object.values(SubmissionStatus).map((status) => [
            status,
            useTranslatedStatus(status),
        ]),
        type: "checkbox",
        initial: [],
    };
    const facultyFilter: UUListTypes.FilterDefinition = {
        field: "faculties",
        label: t("Faculty"),
        options: facultyOptions.value.map((faculty) => [
            faculty.id,
            useTranslateableAttribute(faculty, "label"),
        ]),
        type: "checkbox",
        initial: [],
    };
    return [facultyFilter, statusFilter];
});
</script>

<template>
    <SharedGraphQLList
        v-if="!facultyLoading"
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
                            {{ $t("Ref. number") }}
                        </th>
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
                        <td>
                            {{ row.reference }}
                        </td>
                        <td class="align-middle">
                            <NuxtLink
                                :to="{
                                    name: 'studies-studyId',
                                    params: { studyId: row.id },
                                }"
                            >
                                {{ row.title }}
                            </NuxtLink>
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
                            {{ $t("No results found") }}
                        </td>
                    </tr>
                </tbody>
            </table>
        </template>
    </SharedGraphQLList>
</template>
