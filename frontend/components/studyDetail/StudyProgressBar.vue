<script setup lang="ts">
import { useQuery } from "@vue/apollo-composable";
import { graphql } from "~/generated/gql";
import { useI18n } from "vue-i18n";
import { useLocalDateTime } from "~/composables/useLocalisation";
import { useTranslatedStatus } from "~/composables/useTranslatedStatus";
import { SubmissionStatus } from "~/generated/gql/graphql";
import Loading from "~/components/shared/Loading.vue";

const props = defineProps<{
    studyId: string;
}>();

const GET_STUDY_STATUSES = graphql(`
    query GetStudyStatuses($id: ID!) {
        study(id: $id, mrPermission: "View") {
            statuses {
                status
                createdAt
            }
        }
    }
`);

const { result, loading } = useQuery(GET_STUDY_STATUSES, () => ({
    id: props.studyId,
}));

const statuses = computed(() => result.value?.study?.statuses ?? []);

const { t } = useI18n();

const progressItems = computed(() => {
    const statusBubbleLabels: Record<string, string> = {
        [SubmissionStatus.Draft]: t("Returned to submitter"),
        [SubmissionStatus.Submitted]: t("Submitted"),
    };
    const items = statuses.value.map((change, index) => ({
        // The first draft will read as created
        label: index === 0 ? t("Created") : statusBubbleLabels[change.status],
        // Add the createdAt as the date, except if last status is draft, then just say "Now"
        createdAt: useLocalDateTime(change.createdAt) || null,
        // Submitted is always completed, the last item is always incomplete
        // and the first ("Created") will always be complete
        isComplete:
            change.status === SubmissionStatus.Submitted ||
            index < statuses.value.length - 1 ||
            index === 0,
        isDisabled: false,
    }));
    // Add a "fake" Draft bubble when we only have one status change ("Created")
    if (statuses.value.length === 1) {
        items.push({
            label: t("Draft"),
            createdAt: t("Now"),
            isComplete: false,
            isDisabled: false,
        });
    }
    // If the most recent status is Draft, add a "fake" future submitted status
    if (statuses.value.at(-1)?.status === SubmissionStatus.Draft) {
        items.push({
            label: t("Submitted"),
            createdAt: null,
            isComplete: false,
            isDisabled: true,
        });
    }
    return items;
});
</script>

<template>
    <div v-if="loading">
        <Loading />
    </div>
    <div v-else-if="progressItems.length > 1" class="stepper h-100">
        <ul class="h-100 d-flex flex-column justify-content-between">
            <li v-for="(progressItem, index) in progressItems" :key="index">
                <a
                    class="stepper-item"
                    :class="{ disabled: progressItem.isDisabled }"
                >
                    <span
                        class="stepper-bubble stepper-bubble-largest"
                        :class="{
                            complete: progressItem.isComplete,
                            incomplete:
                                !progressItem.isComplete &&
                                !progressItem.isDisabled,
                        }"
                    ></span>
                    <span class="d-flex flex-column">
                        <span class="lh-1">{{ $t(progressItem.label) }}</span>
                        <span
                            v-if="progressItem.createdAt"
                            style="font-size: 0.7em; line-height: 1.3"
                            class="text-muted"
                        >
                            {{ progressItem.createdAt }}
                        </span>
                    </span>
                </a>
            </li>
        </ul>
    </div>
</template>
