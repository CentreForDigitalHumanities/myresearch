<script lang="ts" setup>
import type { RepeatableStepQuestionWithValue } from "~/composables/useProcessForm";
import { useSubmissionId, useStudyId } from "~/composables/useRouteParams";
import FormLabel from "../form/FormLabel.vue";
import { BSButton } from "cdh-vue-lib";
import { useMutation } from "@vue/apollo-composable";
import { graphql } from "~/generated/gql";
import { useNotification } from "~/composables/useNotification";
import { useI18n } from "vue-i18n";
import { useTranslateableAttribute } from "~/composables/useLocalisation";
import { computed } from "vue";
import { useQuery } from "@vue/apollo-composable";

const submissionId = useSubmissionId();
const studyId = useStudyId();
const { t } = useI18n();

interface Props {
    question: RepeatableStepQuestionWithValue;
    isInvalid: boolean;
}

const props = defineProps<Props>();

const CREATE_STEP_REPEAT_MUTATION = graphql(`
    mutation CreateStepRepeat(
        $userFormId: ID!
        $repeatableId: ID!
        $responseId: ID
    ) {
        createRepeat(
            userFormId: $userFormId
            repeatableId: $repeatableId
            responseId: $responseId
        ) {
            newRepeatIndex
            errors {
                field
                messages
            }
        }
    }
`);

const GET_REPEATABLE_STEP_QUERY = graphql(`
    query GetRepeatableStepsWithRepeats($repeatableId: ID!, $responseId: ID) {
        repeatableStepsWithRepeats(
            repeatableId: $repeatableId
            responseId: $responseId
        ) {
            stepId
            nameNl
            nameEn
            slug
            background
            repeatIndex
        }
    }
`);

const DELETE_STEP_REPEAT_MUTATION = graphql(`
    mutation DeleteStepRepeat(
        $userFormId: ID!
        $repeatId: ID!
        $responseId: ID!
    ) {
        deleteRepeat(
            userFormId: $userFormId
            repeatId: $repeatId
            responseId: $responseId
        ) {
            ok
            errors {
                field
                messages
            }
        }
    }
`);

const { mutate: createStepRepeat } = useMutation(CREATE_STEP_REPEAT_MUTATION, {
    update: (cache) => {
        cache.evict({ fieldName: "form" });
        cache.evict({ fieldName: "repeatableStepsWithRepeats" });
        cache.gc();
    },
});

const { mutate: deleteStepRepeat } = useMutation(DELETE_STEP_REPEAT_MUTATION, {
    update: (cache) => {
        cache.evict({ fieldName: "form" });
        cache.evict({ fieldName: "repeatableStepsWithRepeats" });
        cache.gc();
    },
});

const { result: repeatableStepResult } = useQuery(
    GET_REPEATABLE_STEP_QUERY,
    () => ({
        repeatableId: props.question.repeatableStepId,
        responseId: props.question.responseId,
    }),
);

const repeatableSteps = computed(() =>
    (repeatableStepResult.value?.repeatableStepsWithRepeats || []).filter(
        (step) => step !== null,
    ),
);

function handleAddStep(): void {
    const userFormId = submissionId.value;
    if (!userFormId) {
        return;
    }

    void createStepRepeat({
        userFormId,
        repeatableId: props.question.repeatableStepId,
        responseId: props.question.responseId,
    }).catch(() => {
        useNotification(
            t("An error occurred while adding a step. Please try again."),
            "danger",
        );
    });
}

function handleDeleteStep(repeatId: string): void {
    const userFormId = submissionId.value;
    if (!userFormId) {
        return;
    }

    // There should always be a response available when deleting
    const responseId = props.question.responseId;
    if (!responseId) {
        return;
    }

    void deleteStepRepeat({
        userFormId,
        repeatId,
        responseId: responseId,
    }).catch(() => {
        useNotification(
            t("An error occurred while deleting a step. Please try again."),
            "danger",
        );
    });
}

function navigateToStep(slug: string) {
    return navigateTo({
        name: "studies-studyId-submissionId-slug",
        params: {
            studyId: studyId.value,
            submissionId: submissionId.value,
            slug: slug,
        },
    });
}
</script>

<template>
    <div>
        <FormLabel :question="question" />
        <div
            v-if="question.descriptionNl || question.descriptionEn"
            class="text-muted"
            v-html="useTranslateableAttribute(question, 'description')"
        ></div>
        <div v-if="repeatableSteps.length > 0">
            <div
                v-for="(step, index) in repeatableSteps"
                :key="`${step.stepId}-${step.repeatIndex}`"
            >
                <div
                    class="border rounded p-3 mb-1 d-flex justify-content-between align-items-center"
                >
                    <div>
                        <h5 class="mb-1">
                            {{ useTranslateableAttribute(step, "name") }} -
                            {{ index + 1 }} - {{ step.repeatIndex }}
                        </h5>
                    </div>

                    <div class="d-flex gap-2">
                        <button
                            class="btn btn-primary"
                            @click.prevent="
                                navigateToStep(
                                    `${step.slug}.${step.repeatIndex}`,
                                )
                            "
                        >
                            {{ $t("Edit") }}
                        </button>
                        <button
                            class="btn btn-secondary"
                            @click.prevent="
                                handleDeleteStep(String(step.repeatIndex))
                            "
                        >
                            {{ $t("Delete") }}
                        </button>
                    </div>
                </div>
            </div>
        </div>
        <div v-else>
            <div
                class="p-3 mb-1 d-flex justify-content-center align-items-center"
            >
                {{ $t("No steps added yet ...") }}
            </div>
        </div>
        <BSButton
            variant="primary"
            class="w-100 align-self-stretch"
            @click="handleAddStep"
        >
            {{ $t("Click to add a step") }}
        </BSButton>
    </div>
</template>
