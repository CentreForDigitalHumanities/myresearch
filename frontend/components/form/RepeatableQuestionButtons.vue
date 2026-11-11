<script lang="ts">
import { BSButton } from "cdh-vue-lib";
import { useMutation } from "@vue/apollo-composable";
import { graphql } from "~/generated/gql";
import { useNotification } from "~/composables/useNotification";
import { X } from "lucide-vue-next";
import type { ApolloCache } from "@apollo/client/core";
import { useI18n } from "vue-i18n";

const CREATE_QUESTION_REPEAT_MUTATION = graphql(`
    mutation MRFormCreateQuestionRepeat(
        $input: CreateQuestionRepeatMutationInput!
    ) {
        createQuestionRepeat(input: $input) {
            newRepeatIndex
            errors {
                field
                messages
            }
        }
    }
`);

const DELETE_QUESTION_REPEAT_MUTATION = graphql(`
    mutation MRFormDeleteQuestionRepeat($input: DeleteRepeatMutationInput!) {
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
interface Props {
    question: QuestionWithValue;
    step: CombinedStepWithValues;
}

const props = defineProps<Props>();

const submissionId = useSubmissionId();
const { t } = useI18n();

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
}

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
                questionId: question.questionId,
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
    const userSubmissionId = submissionId.value;
    if (
        !userSubmissionId ||
        question.repeatIndex === null ||
        question.repeatIndex === undefined
    ) {
        return;
    }

    try {
        await mutateFormSubmission(props.step, userSubmissionId, {
            reloadStudy: false,
            // The form is reloaded after the delete mutation.
            reloadForm: false,
        });
        await deleteQuestionRepeat({
            input: {
                submissionId: userSubmissionId,
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
</script>

<template>
    <button
        v-if="question.isRepeatable && !isOnlyOccurrence(question)"
        type="button"
        class="text-danger link-underline-danger border-0"
        @click="handleDeleteRepeat(question)"
    >
        <div class="d-flex align-items-center">
            <X class="icon" />
            <div class="ml-3">{{ t("Delete") }}</div>
        </div>
    </button>
    <BSButton
        v-if="question.isRepeatable && isLastOccurrence(question)"
        type="button"
        variant="primary"
        class="w-100 align-self-stretch mt-3"
        @click="handleAddRepeat(question)"
    >
        {{ $t("Click to add another") }}
    </BSButton>
</template>
