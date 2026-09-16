<script lang="ts" setup>
import { useI18n } from "vue-i18n";
import { useDisplayFileSize } from "~/composables/useDisplayFileSize";
import type {
    CombinedStepWithValues,
    QuestionWithValue,
} from "~/composables/useProcessForm";
import { useSelectLabel } from "~/composables/useSelectLabel";

interface Props {
    step: CombinedStepWithValues;
}

defineProps<Props>();

const { t } = useI18n();

const notAnswered = computed(() => t("Not answered"));

function getFileName(question: FileUploadQuestionWithValue): string {
    if (!question.value) {
        return notAnswered.value;
    }
    return `${question.value.name} (${useDisplayFileSize(question.value.size)})`;
}

function formatAnswer(question: QuestionWithValue): string {
    const value = question.value;

    switch (question.__typename) {
        case "TrueFalseQuestionType":
            return value ? t("Yes") : t("No");
        case "SelectQuestionType":
            return useSelectLabel(question) ?? notAnswered.value;
        case "FileUploadQuestionType":
            return getFileName(question);
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
    <div class="border rounded overflow-hidden">
        <div
            v-for="(question, index) in step.questions"
            :key="`${question.questionId}-${question.repeatIndex}`"
            class="row g-0"
            :class="{ 'border-bottom': index < step.questions.length - 1 }"
        >
            <div class="col-md-5 fst-italic border-end px-3 py-2">
                {{ useTranslateableAttribute(question, "text") }}&nbsp;<span
                    v-if="question.required"
                    class="text-danger"
                    >*</span
                >
            </div>
            <div
                class="col-md-7 preserve-white-space px-3 py-2"
                :class="{
                    'text-danger': (question.errors?.length ?? 0) > 0,
                }"
            >
                {{ formatAnswer(question) }}
            </div>
        </div>
    </div>
</template>

<style scoped>
.preserve-white-space {
    white-space: pre-wrap;
}
</style>
