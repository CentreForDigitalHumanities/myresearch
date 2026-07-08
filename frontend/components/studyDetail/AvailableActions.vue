<script setup lang="ts">
import { useI18n } from "vue-i18n";
import { useMutation, useQuery } from "@vue/apollo-composable";
import {
    PencilLine,
    Trash2,
    SquareCheckBig,
    SquareDashed,
} from "lucide-vue-next";
import type { Component } from "vue";
import { graphql } from "~/generated/gql";
import type { GetFirstSlugAndActionsQuery } from "~/generated/gql/graphql";
import { ActionEnum } from "~/generated/gql/graphql";
import { NuxtLink } from "#components";
import { useConfirm } from "cdh-vue-lib";
import type { RouteParamsRawGeneric } from "vue-router";
import Loading from "~/components/shared/Loading.vue";

type AvailableAction = {
    label: string;
    callback: () => void;
    icon?: Component;
    hidden?: boolean;
    style?: Record<string, string>;
};

const props = defineProps<{
    studyId: string;
    submissionId: string;
}>();

const GET_FIRST_SLUG_AND_ACTIONS = graphql(`
    query GetFirstSlugAndActions($studyId: ID!, $submissionId: ID!) {
        form(submissionId: $submissionId, mrPermission: "View") {
            formId
            steps {
                stepId
                slug
            }
        }
        study(id: $studyId, mrPermission: "View") {
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

const { t } = useI18n();

const MARK_STUDY_SEEN_MUTATION = graphql(`
    mutation MarkStudySeen($studyId: ID!, $isSeen: Boolean!) {
        updateStudySeen(id: $studyId, isSeen: $isSeen) {
            study {
                id
            }
            errors {
                field
                messages
            }
        }
    }
`);

const { mutate: markStudySeen } = useMutation(MARK_STUDY_SEEN_MUTATION);

function checkMarkStudySeen(isSeen: boolean): void {
    useConfirm({
        text: t("Do you want to mark this study as seen?"),
        confirmText: t("Yes"),
        abortText: t("No"),
        headerText: t("Confirm new registration"),
        callback: () => {
            markStudySeen({ studyId: props.studyId, isSeen: isSeen })
                .then((result) => {
                    if (result?.data?.updateStudySeen?.ok) {
                        useNotification(
                            t("Study updated successfully."),
                            "success",
                        );
                        location.reload();
                    } else {
                        useNotification(t("Failed to update study."), "danger");
                    }
                })
                .catch(() => {
                    useNotification(t("Failed to update study."), "danger");
                });
        },
    });
}
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

const { mutate: markStudySeen } = useMutation(DELETE_STUDY, {
    update: (cache) => {
        cache.evict({ fieldName: "studyPages" });
        cache.gc();
    },
});

function deleteStudyWithConfirmation(): void {
    useConfirm({
        text: t("Are you sure you want to delete this study?"),
        confirmText: t("Yes"),
        abortText: t("No"),
        headerText: t("Confirm study deletion"),
        callback: () => {
            markStudySeen({ id: props.studyId })
                .then((result) => {
                    if (result?.data?.deleteStudy?.ok) {
                        useNotification(
                            t("Study deleted successfully."),
                            "success",
                        );
                        void navigateTo("/studies");
                    } else {
                        useNotification(t("Failed to delete study."), "danger");
                    }
                })
                .catch(() => {
                    useNotification(t("Failed to delete study."), "danger");
                });
        },
    });
}

const actionMap = computed<Record<ActionEnum, AvailableAction>>(() => ({
    [ActionEnum.EditAction]: {
        label: t("Continue editing"),
        icon: PencilLine,
        hidden: slug.value === null,
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
    [ActionEnum.MarkSeenAction]: {
        label: t("Mark as seen"),
        callback: () => {
            checkMarkStudySeen(true);
        },
        icon: SquareCheckBig,
        style: {
            "--bs-tiles-hover-bg": "var(--bs-info)",
            "--bs-tiles-hover-color": "var(--bs-white)",
        },
    },
    [ActionEnum.MarkUnseenAction]: {
        label: t("Mark as unseen"),
        callback: () => {
            checkMarkStudySeen(false);
        },
        icon: SquareDashed,
        style: {
            "--bs-tiles-hover-bg": "var(--bs-secondary)",
            "--bs-tiles-hover-color": "var(--bs-white)",
        },
    },
}));

const availableActions = computed<AvailableAction[]>(() => {
    const studyActions = result.value?.study?.actions;
    if (!studyActions) {
        return [];
    }
    return studyActions
        .map((actionEnum: ActionEnum) => actionMap.value[actionEnum])
        .filter((action) => action.hidden !== true);
});
</script>

<template>
    <div v-if="loading">
        <Loading />
    </div>
    <div v-else-if="availableActions.length > 0">
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
