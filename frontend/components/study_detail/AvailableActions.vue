<script setup lang="ts">
import { useI18n } from "vue-i18n";
import { useQuery } from "@vue/apollo-composable";
import { PencilLine, Trash2 } from "lucide-vue-next";
import type { Component } from "vue";
import { graphql } from "~/generated/gql";
import type { GetFirstSlugAndActionsQuery } from "~/generated/gql/graphql";
import Loading from "~/components/shared/Loading.vue";
import { ActionEnum } from "~/generated/gql/graphql";
import { NuxtLink } from "#components";
import type { RouteParamsRawGeneric } from "vue-router";


type AvailableAction = {
    label: string;
    name: string;
    params: RouteParamsRawGeneric;
    icon?: Component;
    style?: Record<string, string>;
};

const props = defineProps<{
  studyId: string;
    submissionId: string;
}>();

const GET_FIRST_SLUG_AND_ACTIONS = graphql(`
    query GetFirstSlugAndActions($studyId: ID!, $submissionId: ID!) {
        form(submissionId: $submissionId, mrPermission: "Edit") {
            formId
            steps {
                stepId
                slug
            }
        }
        study(id: $studyId, mrPermission: "Edit") {
            id
            actions
        }
    }
`);

const { result } = useQuery<GetFirstSlugAndActionsQuery>(
    GET_FIRST_SLUG_AND_ACTIONS,
    () => ({
        submissionId: props.submissionId,
        studyId: props.studyId,
    }),
);

const slug = computed<string | null>(() => {
    const firstStep = result.value?.form?.steps[0];
    return firstStep?.slug || null;
});

const isSlugLoaded = computed(() => slug.value !== null);

const { t } = useI18n();

const handleActionClick = (action: AvailableAction) => {
    void navigateTo({ name: action.name, params: action.params });
};

const actionMap = computed<Record<ActionEnum, AvailableAction>>(() => ({
    [ActionEnum.EditAction]: {
        label: t("Continue editing"),
        name: "procreg-submissionId-slug",
        params: { submissionId: props.submissionId, slug: slug.value },
        icon: PencilLine,
    },
    [ActionEnum.DeleteAction]: {
        label: t("Delete"),
        name: "studies-studyId-delete",
        params: { studyId: props.studyId },
        icon: Trash2,
        style: {
            "--bs-tiles-hover-bg": "var(--bs-danger)",
            "--bs-tiles-hover-color": "var(--bs-white)",
        },
    },
}));

const availableActions = computed<AvailableAction[]>(() => {
    const studyActions = result.value?.study?.actions;
    if (studyActions) {
        return studyActions.map(
            (actionEnum: ActionEnum) => actionMap.value[actionEnum],
        );
    }
    return [];
});
</script>

<template>
    <div v-if="!isSlugLoaded">
        <loading />
    </div>
    <div v-else-if="availableActions.length > 0">
        <h3 class="mb-3">{{ $t("Available actions") }}:</h3>
        <div class="tiles">
            <NuxtLink
                v-for="(action, index) in availableActions"
                :key="index"
                :style="action.style"
                class="tile h-100 justify-content-around"
                @click.prevent="handleActionClick(action)"
            >
                <strong class="text-center">{{ $t(action.label) }}</strong>
                <component :is="action.icon" v-if="action.icon"> </component>
            </NuxtLink>
        </div>
    </div>
    <h3 v-else>{{ $t("No actions available") }}</h3>
</template>
