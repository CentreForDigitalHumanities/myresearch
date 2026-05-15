<script lang="ts" setup>
import { useI18n } from "vue-i18n";
import { SubmissionStatus } from "~/generated/gql/graphql";

interface Props {
    status: SubmissionStatus;
}

const props = defineProps<Props>();

const { t } = useI18n();

const STATUS_MAP: Record<
    SubmissionStatus,
    { label: string; colorClass: string }
> = {
    [SubmissionStatus.Draft]: { label: t("Draft"), colorClass: "text-bg-gray" },
    [SubmissionStatus.Submitted]: {
        label: t("Submitted"),
        colorClass: "text-bg-primary",
    },
    [SubmissionStatus.Approved]: {
        label: t("Approved"),
        colorClass: "text-bg-success",
    },
    [SubmissionStatus.Rejected]: {
        label: t("Rejected"),
        colorClass: "text-bg-danger",
    },
};
</script>

<template>
    <span :class="`badge rounded-pill ${STATUS_MAP[props.status].colorClass}`">
        {{ STATUS_MAP[props.status].label }}
    </span>
</template>
