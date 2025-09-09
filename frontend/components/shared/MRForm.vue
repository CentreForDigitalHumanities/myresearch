<script lang="ts" setup>
import type { QuestionType } from "~/generated/gql/graphql";
import {
    SharedDateQuestion,
    SharedFormSideBar,
    SharedSelectQuestion,
    SharedTextQuestion,
} from "#components";
import type { CombinedForm } from "./FormWrapper.vue";
import type { Component } from "vue";

type QuestionTypeWithTypeName = Pick<QuestionType, "__typename">;

interface Props {
    form: CombinedForm;
}
defineProps<Props>();

const questionComponentMap: Record<
    QuestionType["__typename"],
    Component | null
> = {
    TextQuestionType: SharedTextQuestion,
    SelectQuestionType: SharedSelectQuestion,
    DateQuestionType: SharedDateQuestion,
    FileUploadQuestionType: null,
    NumberQuestionType: null,
    TrueFalseQuestionType: null,
};

function getQuestionComponent(
    question: QuestionTypeWithTypeName,
): Component | null {
    return questionComponentMap[question.__typename];
}
</script>

<template>
    <h2>{{ useTranslateableAttribute(form, "name") }}</h2>
    <p>{{ useTranslateableAttribute(form, "description") }}</p>
    <div class="uu-form-row">
        <div class="d-flex flex-column">
            <div v-for="question in form.questions" :key="question.id">
                <component
                    :is="getQuestionComponent(question)"
                    v-if="getQuestionComponent(question) !== null"
                    :question="question"
                />
                <p v-else class="my-3">
                    {{ question.__typename }} does not have a component yet. 😢
                </p>
            </div>
        </div>
        <SharedFormSideBar :form="form" />
    </div>
</template>
