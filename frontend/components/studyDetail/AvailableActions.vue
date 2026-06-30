<script setup lang="ts">
import { useI18n } from "vue-i18n";
import { useMutation, useQuery } from "@vue/apollo-composable";
import { PencilLine, Trash2 } from "lucide-vue-next";
import type { Component } from "vue";
import { graphql } from "~/generated/gql";
import type { GetFirstSlugAndActionsQuery } from "~/generated/gql/graphql";
import { ActionEnum } from "~/generated/gql/graphql";
import { NuxtLink } from "#components";
import { useConfirm } from "cdh-vue-lib";

type AvailableAction = {
    label: string;
    callback: () => void;
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

const { result, loading } = useQuery<GetFirstSlugAndActionsQuery>(
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

const DELETE_STUDY = graphql(`
    mutation StudyDetailDeleteStudy($id: ID!) {
        deleteStudy(id: $id) {
            ok
            errors {
                field
                messages
            }
        }
    }
`);

const { mutate: deleteStudy } = useMutation(DELETE_STUDY, {
    update: (cache) => {
        cache.evict({ fieldName: "studyPages" });
        cache.gc();
    },
});

function deleteStudyWithConfirmation(): void {
    useConfirm({
        text: t("Are you sure you want to delete this study?"),
        callback: () => {
            deleteStudy({ id: props.studyId })
                .then((result) => {
                    if (result?.data?.deleteStudy?.ok) {
                        useNotification(
                            "Study deleted successfully",
                            "success",
                        );
                        void navigateTo("/studies");
                    } else {
                        useNotification(
                            "Failed to delete study. Please try again.",
                            "danger",
                        );
                    }
                })
                .catch(() => {
                    useNotification(
                        "Failed to delete study. Please try again.",
                        "danger",
                    );
                });
        },
    });
}

const actionMap = computed<Record<ActionEnum, AvailableAction>>(() => ({
    [ActionEnum.EditAction]: {
        label: t("Continue editing"),
        icon: PencilLine,
        callback: () => {
            void navigateTo({
                name: "studies-studyId-submissionId-slug",
                params: {
                    studyId: props.studyId,
                    submissionId: props.submissionId,
                    slug: slug.value,
                },
            });
        },
    },
    [ActionEnum.DeleteAction]: {
        label: t("Delete"),
        icon: Trash2,
        callback: deleteStudyWithConfirmation,
        style: {
            "--bs-tiles-hover-bg": "var(--bs-danger)",
            "--bs-tiles-hover-color": "var(--bs-white)",
        },
    },
}));

const availableActions = computed<AvailableAction[]>(() => {
    const studyActions = result.value?.study?.actions;
    if (!studyActions) {
        return [];
    }
    return studyActions.map(
        (actionEnum: ActionEnum) => actionMap.value[actionEnum],
    );
});
</script>

<template>
    <div v-if="loading">
        <loading />
    </div>
    <div v-else-if="isSlugLoaded && availableActions.length > 0">
        <h3 class="mb-3">{{ $t("Available actions") }}:</h3>
        <div class="tiles">
            <NuxtLink
                v-for="(action, index) in availableActions"
                :key="index"
                :style="action.style"
                class="tile h-100 justify-content-around"
                @click.prevent="action.callback"
            >
                <strong class="text-center">{{ $t(action.label) }}</strong>
                <component :is="action.icon" v-if="action.icon"> </component>
            </NuxtLink>
        </div>
    </div>
    <h3 v-else>{{ $t("No actions available") }}</h3>
</template>
