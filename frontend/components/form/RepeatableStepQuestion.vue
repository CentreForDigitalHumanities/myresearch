<script lang="ts" setup>
import type { RepeatableStepQuestionWithValue } from "~/composables/useProcessForm";
import { useSubmissionId } from "~/composables/useRouteParams";
import FormLabel from "../form/FormLabel.vue";
import { BSButton } from "cdh-vue-lib";
import { useMutation } from "@vue/apollo-composable";
import { graphql } from "~/generated/gql";
import { useNotification } from "~/composables/useNotification";
import { useI18n } from "vue-i18n";
import { useTranslateableAttribute } from "~/composables/useLocalisation";
import { computed } from "vue";
import { useQuery } from "@vue/apollo-composable";
import Loading from "~/components/shared/Loading.vue";
import type { ApolloCache } from "@apollo/client/core";
import { Repeatable } from "~/generated/gql/graphql.ts";

interface Props {
    question: RepeatableStepQuestionWithValue;
    parentRepeatIndex?: number | null;
    isInvalid: boolean;
}

const props = defineProps<Props>();
const emit = defineEmits<{
    (e: "repeat-step-clicked", slug: string): void;
}>();

const currentSubmissionId = useSubmissionId();
const { t } = useI18n();

const CREATE_STEP_REPEAT_MUTATION = graphql(`
    mutation CreateStepRepeat($input: CreateRepeatMutationInput!) {
        createRepeat(input: $input) {
            newRepeatIndex
            errors {
                field
                messages
            }
        }
    }
`);

const GET_REPEATABLE_STEP_QUERY = graphql(`
    query GetRepeatableStepsWithRepeats(
        $repeatableId: ID!
        $submissionId: ID!
        $repeatIndices: [ID!]!
    ) {
        repeatableStepsWithRepeats(
            repeatableId: $repeatableId
            submissionId: $submissionId
            repeatIndices: $repeatIndices
        ) {
            stepId
            nameNl
            nameEn
            slug
            repeatIndex
        }
    }
`);

const DELETE_STEP_REPEAT_MUTATION = graphql(`
    mutation DeleteStepRepeat($input: DeleteRepeatMutationInput!) {
        deleteRepeat(input: $input) {
            ok
            errors {
                field
                messages
            }
        }
    }
`);

const { mutate: createStepRepeat } = useMutation(CREATE_STEP_REPEAT_MUTATION, {
    update: postUpdateCacheEvict,
});

const { mutate: deleteStepRepeat } = useMutation(DELETE_STEP_REPEAT_MUTATION, {
    update: postUpdateCacheEvict,
});

function postUpdateCacheEvict(cache: ApolloCache<unknown>): void {
    cache.evict({ fieldName: "form" });
    cache.evict({ fieldName: "repeatableStepsWithRepeats" });
    cache.gc();
}

const repeatIndices = computed(() => {
    try {
        const parsed = JSON.parse(props.question.answer as string) as {
            value?: string[];
        };
        return parsed.value || [];
    } catch {
        return [];
    }
});

const { result: repeatableStepResult } = useQuery(
    GET_REPEATABLE_STEP_QUERY,
    () => ({
        submissionId: currentSubmissionId.value ?? "",
        repeatableId: props.question.repeatableStepId,
        repeatIndices: repeatIndices.value,
    }),
);

const repeatableSteps = computed(
    () => repeatableStepResult.value?.repeatableStepsWithRepeats ?? [],
);

function handleAddStep(): void {
    const submissionId = currentSubmissionId.value;
    if (!submissionId) {
        return;
    }

    void createStepRepeat({
        input: {
            submissionId,
            repeatableType: Repeatable.Step,
            objectId: props.question.repeatableStepId,
            parentId: props.parentRepeatIndex?.toString() ?? null,
        },
    }).catch(() => {
        useNotification(
            t("An error occurred while adding a step. Please try again."),
            "danger",
        );
    });
}

function handleDeleteStep(repeatIndexId: number): void {
    const userFormId = currentSubmissionId.value;
    if (!userFormId) {
        return;
    }

    void deleteStepRepeat({
        input: {
            userFormId,
            repeatIndexId: repeatIndexId.toString(),
        },
    }).catch(() => {
        useNotification(
            t("An error occurred while deleting a step. Please try again."),
            "danger",
        );
    });
}
</script>

<template>
    <div>
        <FormLabel :question="question" />
        <div
            class="text-muted"
            v-html="useTranslateableAttribute(question, 'description')"
        ></div>
        <Loading v-if="!repeatableStepResult" />
        <template v-else-if="repeatableSteps.length > 0">
            <div
                v-for="step in repeatableSteps"
                :key="`${step.stepId}-${step.repeatIndex}`"
                class="border rounded p-3 mb-1 d-flex justify-content-between align-items-center"
            >
                <div>
                    <h5 class="mb-1">
                        {{ useTranslateableAttribute(step, "name") }}
                    </h5>
                </div>
                <div class="d-flex gap-2">
                    <button
                        class="btn btn-primary"
                        @click.prevent="
                            emit(
                                'repeat-step-clicked',
                                `${step.slug}.${step.repeatIndex}`,
                            )
                        "
                    >
                        {{ $t("Edit") }}
                    </button>
                    <button
                        v-if="step.repeatIndex"
                        class="btn btn-secondary"
                        @click.prevent="handleDeleteStep(step.repeatIndex)"
                    >
                        {{ $t("Delete") }}
                    </button>
                </div>
            </div>
        </template>
        <div
            v-else
            class="p-3 mb-1 d-flex justify-content-center align-items-center"
        >
            {{ useTranslateableAttribute(question, "noneYetText") }}
        </div>
        <BSButton
            variant="primary"
            class="w-100 align-self-stretch"
            @click="handleAddStep"
        >
            {{ useTranslateableAttribute(question, "createText") }}
        </BSButton>
    </div>
</template>
