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
import type {
    CombinedStepWithValues,
    QuestionWithValue,
} from "~/composables/useBuildForm";
import type { ErrorObject, Validation } from "@vuelidate/core";

interface Props {
    step: CombinedStepWithValues;
    vuelidate: Validation;
}
const props = defineProps<Props>();

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

function getErrorsForControl(question: QuestionWithValue): ErrorObject[] {
    return props.vuelidate.$errors.filter(
        (error) => error.$propertyPath === question.location,
    );
}

function hasErrors(question: QuestionWithValue): boolean {
    return getErrorsForControl(question).length > 0;
}
</script>

<template>
    <h2>{{ useTranslateableAttribute(step, "name") }}</h2>
    <p>{{ useTranslateableAttribute(step, "description") }}</p>
    <div class="uu-form-row">
        <div class="d-flex flex-column">
            <div
                v-for="question in step.questions"
                :key="question.id"
                class="uu-form-field"
            >
                <component
                    :is="questionComponentMap[question.__typename]"
                    v-model="question.value"
                    :question="question"
                    :is-invalid="hasErrors(question)"
                />
                <div
                    v-for="error of getErrorsForControl(question)"
                    :key="error.$uid"
                    class="invalid-feedback"
                >
                    {{ error.$message }}
                </div>
            </div>
        </div>
        <FormSideBar :step="step" />
    </div>
</template>

<style lang="scss" scoped>
// .invalid-feedback has display: none by default, unless the input element
// directly preceding it has the is-invalid class.
.invalid-feedback {
    display: block;
}
</style>
