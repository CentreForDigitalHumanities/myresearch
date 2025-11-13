<script lang="ts" setup>
import {
    SharedDateQuestion,
    SharedFileUploadQuestion,
    SharedFormSideBar,
    SharedNumberQuestion,
    SharedSelectQuestion,
    SharedTextQuestion,
    SharedTrueFalseQuestion,
} from "#components";
import type { CombinedStep } from "./FormWrapper.vue";
import type { Component } from "vue";

interface Props {
    form: CombinedStep;
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
    <h2>{{ useTranslateableAttribute(form, "name") }}</h2>
    <p>{{ useTranslateableAttribute(form, "description") }}</p>
    <div class="uu-form-row">
        <div class="d-flex flex-column">
            <div v-for="question in form.questions" :key="question.id">
                <component
                    :is="questionComponentMap[question.__typename]"
                    :question="question"
                />
            </div>
        </div>
        <SharedFormSideBar :form="form" />
    </div>
</template>
