<script lang="ts" setup>
import {
    SharedDateQuestion,
    SharedFileUploadQuestion,
    SharedNumberQuestion,
    SharedSelectQuestion,
    SharedTextQuestion,
    SharedTrueFalseQuestion,
} from "#components";
import FormSideBar from "./FormSideBar.vue";
import type { Component } from "vue";
import type { CombinedStepWithValues } from "~/composables/useBuildForm";

interface Props {
    step: CombinedStepWithValues;
}
defineProps<Props>();

// Imported components are treated as 'any', so the linter complains, but there
// is nothing we can do to change this, so we need to assert the type manually.
const questionComponentMap = {
    TextQuestionType: SharedTextQuestion as Component,
    SelectQuestionType: SharedSelectQuestion as Component,
    DateQuestionType: SharedDateQuestion as Component,
    NumberQuestionType: SharedNumberQuestion as Component,
    TrueFalseQuestionType: SharedTrueFalseQuestion as Component,
    FileUploadQuestionType: SharedFileUploadQuestion as Component,
};
</script>

<template>
    <h2>{{ useTranslateableAttribute(step, "name") }}</h2>
    <p>{{ useTranslateableAttribute(step, "description") }}</p>
    <div class="uu-form-row">
        <div class="d-flex flex-column">
            <div v-for="question in step.questions" :key="question.id">
                <component
                    :is="questionComponentMap[question.__typename]"
                    v-model="question.value"
                    :question="question"
                />
            </div>
        </div>
        <FormSideBar :step="step" />
    </div>
</template>
