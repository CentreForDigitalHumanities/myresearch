<script lang="ts" setup>
import type {
    DateQuestionType,
    SelectQuestionType,
    TextQuestionType,
} from "~/generated/gql/graphql";
import type { CombinedStep } from "./MRForm.vue";
import { SharedFormSideBar } from "#components";

type QuestionType = CombinedStep["questions"][number];

interface Props {
    step: CombinedStep;
}
defineProps<Props>();

function isTextQuestion(question: QuestionType): question is TextQuestionType {
    return question.__typename === "TextQuestionType";
}

function isSelectQuestion(
    question: QuestionType,
): question is SelectQuestionType {
    return question.__typename === "SelectQuestionType";
}

function isDateQuestion(question: QuestionType): question is DateQuestionType {
    return question.__typename === "DateQuestionType";
}
</script>

<template>
    <h2>{{ useTranslateableAttribute(step, "name") }}</h2>
    <p>{{ useTranslateableAttribute(step, "description") }}</p>
    <div class="uu-form-row">
        <div class="d-flex flex-column">
            <div v-for="question in step.questions" :key="question.id">
                <SharedTextQuestion
                    v-if="isTextQuestion(question)"
                    :question="question"
                />
                <SharedSelectQuestion
                    v-else-if="isSelectQuestion(question)"
                    :question="question"
                />
                <SharedDateQuestion
                    v-else-if="isDateQuestion(question)"
                    :question="question"
                />
                <p v-else class="my-3">
                    {{ question.__typename }} does not have a component yet. 😢
                </p>
            </div>
        </div>
        <SharedFormSideBar v-if="step.info" :config="step.info" />
    </div>
</template>
