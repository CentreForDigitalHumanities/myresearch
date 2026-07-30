<script lang="ts" setup>
import { useFormQuery } from "~/composables/useFormQuery";
import { useStudyQuery } from "~/composables/useStudyQuery";
import { useNotification } from "~/composables/useNotification";
import FormWrapper from "~/components/form/FormWrapper.vue";
import {
    useStepSlug,
    useSubmissionId,
    useStudyId,
} from "~/composables/useRouteParams";
import { BSButton } from "cdh-vue-lib";
import { useI18n } from "vue-i18n";

const submissionId = useSubmissionId();
const slug = useStepSlug();
const form = useFormQuery(submissionId, "Edit");

const studyId = useStudyId();
const study = useStudyQuery(studyId);
const { t } = useI18n();

const formWrapperRef = ref<{ submitForm: () => void } | null>(null);

function handleBackNavigation() {
    // We call submitForm from our FormWrapper component
    formWrapperRef.value?.submitForm();

    useNotification(t("Your progress has been saved."), "info", 3);
    return navigateTo({
        name: "studies-studyId",
        params: { studyId: studyId.value },
    });
}
</script>

<template>
    <div class="uu-content">
        <Title>{{ study?.reference }} - {{ study?.title }}</Title>
        <div
            class="uu-hero d-flex flex-nowrap justify-content-between align-items-center gap-3"
        >
            <BSButton
                variant="secondary"
                class="btn-arrow-left flex-shrink-0"
                @click="handleBackNavigation"
            >
                {{ $t("Save and go back") }}
            </BSButton>
            <h1 class="mb-0 text-wrap text-break">
                {{ study?.reference }} -
                {{ study?.title }}
            </h1>
        </div>
        <div class="uu-container">
            <FormWrapper
                v-if="form && slug"
                ref="formWrapperRef"
                :queried-form="form"
                :current-step-slug="slug"
                :should-evict-study="slug === 'study'"
            />
        </div>
    </div>
</template>

<style scoped>
.hero-title {
    min-width: 0;
}
</style>
