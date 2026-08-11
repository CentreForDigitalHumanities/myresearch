<script lang="ts" setup>
import { useFormQuery } from "~/composables/useFormQuery";
import { useStudyTitleQuery } from "~/composables/useStudyTitleQuery";
import FormWrapper from "~/components/form/FormWrapper.vue";
import StudyHeroTitle from "~/components/form/StudyHeroTitle.vue";
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
        <StudyHeroTitle v-if="study" :study="study" />
        <div class="uu-container">
            <FormWrapper
                v-if="form && slug"
                :queried-form="form"
                :current-step-slug="slug"
                :reload-study="slug === 'study'"
            />
        </div>
    </div>
</template>
