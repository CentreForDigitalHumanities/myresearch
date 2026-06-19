<script setup lang="ts">
import { useI18n } from "vue-i18n";
import { graphql } from "~/generated/gql";
import { useQuery } from "@vue/apollo-composable";
import type { GetStudyStatusChangesQuery } from "~/generated/gql/graphql";

const props = defineProps<{
    studyId: string;
}>();

const { t } = useI18n();

const GET_STUDY_STATUS_CHANGES = graphql(`
    query GetStudyStatusChanges($studyId: ID!) {
        statusChanges(mrPermission: "View", studyId: $studyId) {
            id
            status
            createdAt
        }
    }
`);

const { result: studyStatusChangesResult } =
    useQuery<GetStudyStatusChangesQuery>(GET_STUDY_STATUS_CHANGES, () => ({
        studyId: props.studyId,
    }));

const studyStatusChanges = computed(
    () => studyStatusChangesResult.value?.statusChanges,
);

type ProgressItem = {
    label: string;
    isActive: boolean;
    isComplete: boolean;
};

// draft scenario

const created: ProgressItem = {
    label: t("Created"),
    isActive: false,
    isComplete: true,
};

const notYetSubmitted: ProgressItem = {
    label: t("Submitted"),
    isActive: true,
    isComplete: false,
};

const notYetReviewed: ProgressItem = {
    label: t("Review from Privacy Officer"),
    isActive: false,
    isComplete: false,
};

const notYetConcluded: ProgressItem = {
    label: t("Conclusion"),
    isActive: false,
    isComplete: false,
};

// Revision scenario

const submitted: ProgressItem = {
    label: notYetSubmitted.label,
    isActive: false,
    isComplete: true,
};

const reviewed: ProgressItem = {
    label: notYetReviewed.label,
    isActive: false,
    isComplete: true,
};

const revisionCreated: ProgressItem = {
    label: t("Revision Created"),
    isActive: false,
    isComplete: true,
};

const activeReview: ProgressItem = {
    label: notYetReviewed.label,
    isActive: true,
    isComplete: false,
};

const draftProgress: ProgressItem[] = [
    created,
    notYetSubmitted,
    notYetReviewed,
    notYetConcluded,
];

const submissionProgress: ProgressItem[] = [
    created,
    submitted,
    activeReview,
    notYetConcluded,
];

const revisionReviewProgress: ProgressItem[] = [
    created,
    submitted,
    reviewed,
    revisionCreated,
    submitted,
    activeReview,
    notYetConcluded,
];

const progressItems = computed(() =>
    studyStatusChanges.value?.length === 2 ? submissionProgress : draftProgress,
);
</script>

<template>
    <div class="stepper h-100">
        <ul class="h-100 d-flex flex-column justify-content-between">
            <li v-for="(progressItem, index) in progressItems" :key="index">
                <a
                    class="stepper-item disabled"
                    :class="{ active: progressItem.isActive }"
                >
                    <span
                        class="stepper-bubble stepper-bubble-largest"
                        :class="{
                            complete: progressItem.isComplete,
                            incomplete:
                                !progressItem.isComplete &&
                                progressItem.isActive,
                        }"
                    ></span>
                    <span class="lh-1">{{ $t(progressItem.label) }}</span>
                </a>
            </li>
        </ul>
    </div>
</template>
