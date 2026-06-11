<script setup lang="ts">
import { useI18n } from "vue-i18n";
import { useMutation, useQuery } from "@vue/apollo-composable";
import { PencilLine, Trash2, SquareCheckBig, SquareDashed } from "lucide-vue-next";
import type { Component } from "vue";
import { graphql } from "~/generated/gql";
import type { GetFirstSlugAndActionsQuery } from "~/generated/gql/graphql";
import { ActionEnum } from "~/generated/gql/graphql";
import { NuxtLink } from "#components";
import { useConfirm } from "cdh-vue-lib";

const { t } = useI18n();

type AvailableAction = {
    label: string;
    actionCallback: () => void;
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

const handleUpdateStudyIsSeen = async (isSeen: boolean) => {
    try {
        const result = await markStudySeen({ studyId: props.studyId, isSeen });

        if (!result?.data) {
            useNotification("No response from server", "danger");
            return;
        }

        if (result.data.updateStudySeen?.errors?.length) {
            useNotification("Failed update to study", "danger");
            return;
        }

        if (result.data.updateStudySeen?.study?.id) {
            useNotification("Study updated successfully", "success");
            location.reload();
        }
    } catch {
        useNotification("Failed update study. Please try again.", "danger");
    }
};

function checkMarkStudySeen(isSeen: boolean): void {
    useConfirm({
        text: t("Do you want to mark this study as seen?"),
        confirmText: t("Yes"),
        abortText: t("No"),
        headerText: t("Confirm new registration"),
        callback: () => {
            void handleUpdateStudyIsSeen(isSeen);
        },
    });
}

const actionMap = computed<Record<ActionEnum, AvailableAction>>(() => ({
    [ActionEnum.EditAction]: {
        label: t("Continue editing"),
        actionCallback: () =>
            void navigateTo({
                name: "studies-studyId-submissionId-slug",
                params: {
                    studyId: props.studyId,
                    submissionId: props.submissionId,
                    slug: slug.value,
                },
            }),
        icon: PencilLine,
    },
    [ActionEnum.DeleteAction]: {
        label: t("Delete"),
        actionCallback: () =>
            void navigateTo({
                name: "studies-studyId-delete",
                params: {
                    studyId: props.studyId,
                },
            }),
        icon: Trash2,
        style: {
            "--bs-tiles-hover-bg": "var(--bs-danger)",
            "--bs-tiles-hover-color": "var(--bs-white)",
        },
    },
    [ActionEnum.MarkSeenAction]: {
        label: t("Mark as seen"),
        actionCallback: () => {
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
        actionCallback: () => {
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
    if (studyActions) {
        return studyActions.map(
            (actionEnum: ActionEnum) => actionMap.value[actionEnum],
        );
    }
    return [];
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
                @click.prevent="action.actionCallback"
            >
                <strong class="text-center">{{ $t(action.label) }}</strong>
                <component :is="action.icon" v-if="action.icon"> </component>
            </NuxtLink>
        </div>
    </div>
    <h3 v-else>{{ $t("No actions available") }}</h3>
</template>
