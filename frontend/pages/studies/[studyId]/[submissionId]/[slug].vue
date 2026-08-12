<script lang="ts" setup>
import { useFormQuery } from "~/composables/useFormQuery";
import FormWrapper from "~/components/form/FormWrapper.vue";
import { useStepSlug, useSubmissionId } from "~/composables/useRouteParams";

const submissionId = useSubmissionId();
const slug = useStepSlug();
const form = useFormQuery(submissionId, "Edit");
</script>

<template>
    <div class="uu-content">
        <Title>{{ $t("Processing Register") }}</Title>
        <div class="uu-hero">
            <h1>{{ $t("Processing Register") }}</h1>
        </div>
        <div class="uu-container">
            <FormWrapper
                v-if="form && slug"
                :queried-form="form"
                :current-step-slug="slug"
            />
        </div>
    </div>
</template>
