<script lang="ts">
import TextQuestion from "./TextQuestion.vue";
import SelectQuestion from "./SelectQuestion.vue";
import DateQuestion from "../form/DateQuestion.vue";
import NumberQuestion from "./NumberQuestion.vue";
import TrueFalseQuestion from "./TrueFalseQuestion.vue";
import FileUploadQuestion from "../form/FileUploadQuestion.vue";
import RepeatableStepQuestion from "../form/RepeatableStepQuestion.vue";
import type { Component } from "vue";
import { BSButton } from "cdh-vue-lib";
import { useMutation } from "@vue/apollo-composable";
import { graphql } from "~/generated/gql";
import { useNotification } from "~/composables/useNotification";
import { X } from "lucide-vue-next";
import type { ApolloCache } from "@apollo/client/core";
import { Repeatable } from "~/generated/gql/graphql.ts";

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

const CREATE_QUESTION_REPEAT_MUTATION = graphql(`
    mutation CreateQuestionRepeat($input: CreateRepeatMutationInput!) {
        createRepeat(input: $input) {
            newRepeatIndex
            errors {
                field
                messages
            }
        }
    }
`);

const DELETE_QUESTION_REPEAT_MUTATION = graphql(`
    mutation DeleteQuestionRepeat($input: DeleteRepeatMutationInput!) {
        deleteRepeat(input: $input) {
            ok
            errors {
                field
                messages
            }
        }
    }
`);
</script>

<script lang="ts" setup>
import type {
    CombinedStepWithValues,
    QuestionWithValue,
} from "~/composables/useProcessForm";
import { useSubmissionId } from "~/composables/useRouteParams";
import { useFormSubmission } from "~/composables/useFormSubmission";
import { useI18n } from "vue-i18n";

interface Props {
    step: CombinedStepWithValues;
}

interface Emits {
    (e: "repeat-step-clicked", slug: string): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();
const { t } = useI18n();
const submissionId = useSubmissionId();

const { submitForm: mutateFormSubmission } = useFormSubmission({
    reloadStudy: false,
    reloadForm: true,
});

const { mutate: createQuestionRepeat } = useMutation(
    CREATE_QUESTION_REPEAT_MUTATION,
    {
        update: evictForm,
    },
);

const { mutate: deleteQuestionRepeat } = useMutation(
    DELETE_QUESTION_REPEAT_MUTATION,
    {
        update: evictForm,
    },
);

function evictForm(cache: ApolloCache<unknown>): void {
    cache.evict({ fieldName: "form" });
    cache.gc();
}

// FileUploadQuestions and questions with conditions are watched. If their
// values change, the form is resubmitted.
const watchedQuestions = computed(() =>
    props.step.questions.filter(
        (question) =>
            question.hasConditions ||
            question.__typename === "FileUploadQuestionType",
    ),
);

// TODO: move repeatables-related logic below to separate component.

// Build a map between question IDs and their last occurrence to show button only once.
const lastOccurrenceByQuestionId = computed(() =>
    props.step.questions.reduce((lastOccurrences, question) => {
        const previous = lastOccurrences.get(question.questionId);

        if (
            !previous ||
            (question.repeatIndex ?? -1) > (previous.repeatIndex ?? -1)
        ) {
            lastOccurrences.set(question.questionId, question);
        }

        return lastOccurrences;
    }, new Map<string, QuestionWithValue>()),
);

function isLastOccurrence(question: QuestionWithValue): boolean {
    return (
        lastOccurrenceByQuestionId.value.get(question.questionId) === question
    );
}

function isOnlyOccurrence(question: QuestionWithValue): boolean {
    const count = props.step.questions.filter(
        (q) => q.questionId === question.questionId,
    ).length;
    return count === 1;
};

function isFirstOccurrence(question: QuestionWithValue): boolean {
    const firstIndex = Math.min(
        ...props.step.questions
            .filter((q) => q.questionId === question.questionId)
            .map((q) => (q.repeatIndex !== null ? Number(q.repeatIndex) : -1)),
    );
    const currentIndex =
        question.repeatIndex !== null ? Number(question.repeatIndex) : -1;
    return currentIndex === firstIndex;
};

async function handleAddRepeat(question: QuestionWithValue): Promise<void> {
    const userFormId = submissionId.value;
    if (!userFormId) {
        return;
    }

    await mutateFormSubmission(props.step, userFormId, {
        reloadStudy: false,
        // The form is reloaded after the create mutation.
        reloadForm: false,
    });
    try {
        await createQuestionRepeat({
            input: {
                submissionId: userFormId,
                repeatableType: Repeatable.Question,
                objectId: question.questionId,
                parentId: props.step.repeatIndex
                    ? props.step.repeatIndex.toString()
                    : null,
            },
        });
    } catch {
        useNotification(
            t("An error occurred while adding a question. Please try again."),
            "danger",
        );
    }
}

async function handleDeleteRepeat(question: QuestionWithValue): Promise<void> {
    const userFormId = submissionId.value;
    if (
        !userFormId ||
        question.repeatIndex === null ||
        question.repeatIndex === undefined
    ) {
        return;
    }

    try {
        await mutateFormSubmission(props.step, userFormId, {
            reloadStudy: false,
            // The form is reloaded after the delete mutation.
            reloadForm: false,
        });
        await deleteQuestionRepeat({
            input: {
                userFormId,
                repeatIndexId: question.repeatIndex.toString(),
            },
        });
    } catch {
        useNotification(
            t("An error occurred while deleting a question. Please try again."),
            "danger",
        );
    }
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
                <a
                    v-if="question.isRepeatable && !isOnlyOccurrence(question)"
                    href="#"
                    class="text-danger"
                    @click="handleDeleteRepeat(question)"
                >
                    <div class="d-flex align-items-center">
                        <X class="icon" />
                        <div class="ml-3">{{ t("Delete") }}</div>
                    </div>
                </a>
                <div v-if="question.isRepeatable && isLastOccurrence(question)">
                    <BSButton
                        variant="primary"
                        class="w-100 align-self-stretch mt-3"
                        @click="handleAddRepeat(question)"
                    >
                        {{ $t("Click to add another") }}
                    </BSButton>
                </div>
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
