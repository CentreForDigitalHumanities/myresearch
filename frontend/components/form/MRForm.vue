<script lang="ts">
import TextQuestion from "./TextQuestion.vue";
import SelectQuestion from "./SelectQuestion.vue";
import DateQuestion from "../form/DateQuestion.vue";
import NumberQuestion from "./NumberQuestion.vue";
import TrueFalseQuestion from "./TrueFalseQuestion.vue";
import FileUploadQuestion from "../form/FileUploadQuestion.vue";
import FormSideBar from "../form/FormSideBar.vue";
import type { Component } from "vue";

// Imported components are treated as 'any', so the linter complains. There is
// nothing we can do to change this, so we need to assert the type manually.
const QUESTION_COMPONENT_MAP = {
    TextQuestionType: TextQuestion as Component,
    SelectQuestionType: SelectQuestion as Component,
    DateQuestionType: DateQuestion as Component,
    NumberQuestionType: NumberQuestion as Component,
    TrueFalseQuestionType: TrueFalseQuestion as Component,
    FileUploadQuestionType: FileUploadQuestion as Component,
} as const;
</script>

<script lang="ts" setup>
import type { CombinedStepWithValues } from "~/composables/useProcessForm";

interface Props {
    step: CombinedStepWithValues;
}

interface Emits {
    (e: "submitForm"): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

// FileUploadQuestions and questions with conditions are watched. If their
// values change, the form is resubmitted.
const watchedQuestions = computed(() =>
    props.step.questions.filter(
        (question) =>
            question.hasConditions ||
            question.__typename === "FileUploadQuestionType",
    ),
);

useWatchQuestions(watchedQuestions, () => {
    emit("submitForm");
});
</script>

<template>
    <div class="uu-form-row">
        <div class="d-flex flex-column">
            <div
                v-for="question in step.questions"
                :key="`${question.questionId}-${question.repeatIndex}`"
                class="uu-form-field"
            >
                <component
                    :is="QUESTION_COMPONENT_MAP[question.__typename]"
                    v-model="question.value"
                    :question="question"
                    :is-invalid="(question.errors?.length ?? 0) > 0"
                />
                <div
                    v-for="error of question.errors ?? []"
                    :key="error.$uid"
                    class="invalid-feedback"
                >
                    {{ error.$message }}
                </div>
            </div>
        </div>
    </div>
</template>

<style lang="scss" scoped>
// .invalid-feedback has display: none by default, unless the input element
// directly preceding it has the is-invalid class.
.invalid-feedback {
    display: block;
}
</style>
