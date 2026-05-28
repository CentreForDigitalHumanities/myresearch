<script lang="ts" setup>
import { useI18n } from "vue-i18n";
import type {
    CombinedStepWithValues,
    QuestionWithValue,
    SelectQuestionWithValue,
} from "~/composables/useProcessForm";

interface Props {
    step: CombinedStepWithValues;
}

defineProps<Props>();

const { t } = useI18n();

const notAnswered = computed(() => t("Not answered"));

function getSelectLabel(question: SelectQuestionWithValue): string {
    const options = question.options;
    const selectedOption = options.find(
        (option) => option.id === question.value,
    );
    return selectedOption
        ? useTranslateableAttribute(selectedOption, "label")
        : notAnswered.value;
}

function formatAnswer(question: QuestionWithValue): string {
    const value = question.value;

    switch (question.__typename) {
        case "TrueFalseQuestionType":
            return value ? t("Yes") : t("No");
        case "SelectQuestionType":
            return getSelectLabel(question);
        case "FileUploadQuestionType":
        case "TextQuestionType":
        case "DateQuestionType":
            return typeof value === "string" && value.trim() !== ""
                ? value
                : notAnswered.value;
        case "NumberQuestionType":
            return typeof value === "number"
                ? value.toString()
                : notAnswered.value;
        default:
            return notAnswered.value;
    }
}
</script>

<template>
    <div
        v-for="question in step.questions"
        :key="`${question.questionId}-${question.repeatIndex}`"
        class="row mb-2"
    >
        <div class="col-md-6 fst-italic">
            {{ useTranslateableAttribute(question, "text") }}&nbsp;<span
                v-if="question.required"
                class="text-danger"
                >*</span
            >
        </div>
        <div
            class="col-md-6 preserve-white-space"
            :class="{
                'text-danger': (question.errors?.length ?? 0) > 0,
            }"
        >
            {{ formatAnswer(question) }}
        </div>
    </div>
</template>

<style scoped>
.preserve-white-space {
    white-space: pre-wrap;
}
</style>
