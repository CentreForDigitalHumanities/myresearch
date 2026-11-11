<script lang="ts">
import TextQuestion from "./TextQuestion.vue";
import SelectQuestion from "./SelectQuestion.vue";
import DateQuestion from "./DateQuestion.vue";
import NumberQuestion from "./NumberQuestion.vue";
import TrueFalseQuestion from "./TrueFalseQuestion.vue";
import FileUploadQuestion from "./FileUploadQuestion.vue";
import RepeatableStepQuestion from "./RepeatableStepQuestion.vue";
import RepeatableQuestionButtons from "./RepeatableQuestionButtons.vue";
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
    RepeatableStepQuestionType: RepeatableStepQuestion as Component,
} as const;
</script>

<script lang="ts" setup>
import type {
    CombinedStepWithValues,
    QuestionWithValue,
} from "~/composables/useProcessForm";
import { useSubmissionId } from "~/composables/useRouteParams";
import { useFormSubmission } from "~/composables/useFormSubmission";

interface Props {
    step: CombinedStepWithValues;
}

interface Emits {
    (e: "repeat-step-clicked", slug: string): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const submissionId = useSubmissionId();

const { submitForm: mutateFormSubmission } = useFormSubmission({
    reloadStudy: false,
    reloadForm: true,
});

// FileUploadQuestions and questions with conditions are watched. If their
// values change, the form is resubmitted.
const watchedQuestions = computed(() =>
    props.step.questions.filter(
        (question) =>
            question.hasConditions ||
            question.__typename === "FileUploadQuestionType",
    ),
);

function isFirstOccurrence(question: QuestionWithValue): boolean {
    const firstIndex = Math.min(
        ...props.step.questions
            .filter((q) => q.questionId === question.questionId)
            .map((q) => (q.repeatIndex != null ? q.repeatIndex : -1)),
    );
    const currentIndex =
        question.repeatIndex != null ? question.repeatIndex : -1;
    return currentIndex === firstIndex;
}

function handleStepNameOverride(question: QuestionWithValue): void {
    if (!question.stepNameOverride) {
        return;
    }
    const userFormId = submissionId.value;
    if (userFormId) {
        void mutateFormSubmission(props.step, userFormId);
    }
}

useWatchQuestions(watchedQuestions, () => {
    const userFormId = submissionId.value;
    if (userFormId) {
        void mutateFormSubmission(props.step, userFormId);
    }
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
                    :parent-repeat-index="step.repeatIndex"
                    :is-invalid="(question.errors?.length ?? 0) > 0"
                    :show-description="
                        !question.isRepeatable || isFirstOccurrence(question)
                    "
                    @repeat-step-clicked="
                        (slug: string) => emit('repeat-step-clicked', slug)
                    "
                    @blur="handleStepNameOverride(question)"
                />
                <RepeatableQuestionButtons :question="question" :step="step" />
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
