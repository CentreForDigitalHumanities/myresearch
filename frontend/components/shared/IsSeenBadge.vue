<script lang="ts" setup>
import { useI18n } from "vue-i18n";

interface Props {
    isSeen: boolean;
}

const props = defineProps<Props>();

const { t } = useI18n();

const isSeenMap = computed<
    Record<string, { label: string; colorClass: string }>
>(() => ({
    true: { label: t("Yes"), colorClass: "text-bg-info" },
    false: { label: t("No"), colorClass: "text-bg-gray" },
}));
</script>

<template>
    <span
        :class="`badge rounded-pill ${isSeenMap[String(props.isSeen)].colorClass}`"
    >
        {{ isSeenMap[String(props.isSeen)].label }}
    </span>
</template>
