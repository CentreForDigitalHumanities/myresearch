<script lang="ts" setup>
import { useFormQuery } from "~/composables/useFormQuery";
import { useStudyTitleQuery } from "~/composables/useStudyTitleQuery";
import FormWrapper from "~/components/form/FormWrapper.vue";
import {
    useStepSlug,
    useSubmissionId,
    useStudyId,
} from "~/composables/useRouteParams";

const submissionId = useSubmissionId();
const slug = useStepSlug();
const form = useFormQuery(submissionId, "Edit");

const studyId = useStudyId();
const study = useStudyTitleQuery(studyId);
</script>

<template>
    <div class="uu-content">
        <Title>{{ study?.reference }} - {{ study?.title }}</Title>
        <div class="uu-hero">
            <h1 class="text-wrap text-break">
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
                :reload-study="slug === 'study'"
            />
        </div>
    </div>
</template>
