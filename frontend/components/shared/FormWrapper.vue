<script lang="ts" setup>
import { computed } from "vue";
import { BSButton } from "cdh-vue-lib";
import type { QueriedForm } from "./FormWrapper";
import FormStepper, { type FormStepperConfig } from "./FormStepper";
import MRForm from "./MRForm.vue";
import { useBuildFormStepperConfig } from "~/composables/useBuildFormStepperConfig";
import { useFormState } from "~/composables/useFormState";
import useVuelidate from "@vuelidate/core";
import { graphql } from "~/generated/gql";
import type {
    UserFormInput,
    ResponseInput,
    UpdateUserFormSubmission,
    GetFormQuery,
} from "~/generated/gql/graphql";
import type { ApolloQueryResult } from "@apollo/client";
import { useMutation } from "@vue/apollo-composable";

interface Props {
    queriedForm: QueriedForm;
    currentStepSlug: string;
    refetchForm: () => Promise<ApolloQueryResult<GetFormQuery>> | undefined;
}
const props = defineProps<Props>();

const queried = computed(() => props.queriedForm);
const { formObject, validationRules } = useFormState(queried);

// Watch for changes in the form and mutate and refetch
// This is just a proof-of-concept and our mutation/refetching strategy needs to
// get refined.
watch(
    formObject,
    () => {
        submitForm();
    },
    { deep: true },
);

const UPDATE_USER_FORM = graphql(`
    mutation SaveFormSubmission(
        $id: ID
        $formConfigId: ID
        $responses: [ResponseInput!]!
    ) {
        updateFormSubmission(
            userFormInput: {
                id: $id
                formConfigId: $formConfigId
                responses: $responses
            }
        ) {
            errors {
                field
                messages
            }
            ok
        }
    }
`);

const { mutate: mutateForm } =
    useMutation<UpdateUserFormSubmission>(UPDATE_USER_FORM);

function submitForm(): void {
    const formData = formObject.value;
    if (formData) {
        const inputData = formDataToMutationInput(formData);
        mutateForm(inputData)
            .then(() => {
                void props.refetchForm();
            })
            .catch((error: unknown) => {
                console.error("Error updating form:", error);
            });
    }
}

function formDataToMutationInput(formData: FormWithValues): UserFormInput {
    // Utility function to transform our form into the expected input for our mutation

    // First collect all questions
    const questions = formData.steps.flatMap(getAllQuestions);

    // Then return out object in its expected form
    return {
        id: props.queriedForm.submissionId ?? null,
        formConfigId: props.queriedForm.formId,
        responses: questions.map(
            (question: QuestionWithValue): ResponseInput => {
                return {
                    answer: JSON.stringify({ value: question.value }),
                    id: question.responseId,
                    questionId: question.questionId,
                    repeatIndex: question.repeatIndex,
                };
            },
        ),
    };
}

const v$ = useVuelidate(
    validationRules,
    computed(() => formObject.value ?? { steps: [] }),
    {
        $autoDirty: true,
    },
);

// Stepper configuration
const formStepperConfig = computed<FormStepperConfig | null>(() =>
    useBuildFormStepperConfig(props.queriedForm, props.currentStepSlug),
);

const allSteps = computed(() => {
    const formValue = formObject.value;
    if (!formValue) {
        return [];
    }
    return getAllSteps(formValue);
});

const selectedStep = computed(() => {
    const steps = allSteps.value;
    if (steps.length <= 0) {
        return null;
    }
    return steps.find(({ slug }) => slug === props.currentStepSlug) ?? null;
});

function getAllSteps(form: FormWithValues): CombinedStepWithValues[] {
    return form.steps.flatMap((step) => {
        const steps: CombinedStepWithValues[] = [step];
        if (step.substeps) {
            steps.push(...step.substeps);
        }
        return steps;
    });
}

/**
 * Returns all questions from a step in a flat list.
 */
function getAllQuestions(
    step: StepWithValues | SubstepWithValues,
): QuestionWithValue[] {
    const ownQuestions = step.questions;

    const subStepQuestions =
        "substeps" in step
            ? (step.substeps?.flatMap(getAllQuestions) ?? [])
            : [];

    return [...ownQuestions, ...subStepQuestions];
}

function findCurrentStepIndex(): number {
    const selectedStepValue = selectedStep.value;
    if (!selectedStepValue) {
        return -1;
    }

    const steps = allSteps.value;
    return steps.findIndex((step) => step.slug === selectedStepValue.slug);
}

function getNextStepSlug(): string {
    if (!selectedStep.value) {
        return props.currentStepSlug;
    }

    const steps = allSteps.value;
    const currentIndex = findCurrentStepIndex();

    if (currentIndex === -1 || currentIndex >= steps.length - 1) {
        // Already at the last step or step not found.
        return props.currentStepSlug;
    }

    return steps[currentIndex + 1].slug;
}

function getPreviousStepSlug(): string {
    if (!selectedStep.value) {
        return props.currentStepSlug;
    }

    const steps = allSteps.value;
    const currentIndex = findCurrentStepIndex();

    if (currentIndex <= 0) {
        // Already at the first step or step not found.
        return props.currentStepSlug;
    }

    return steps[currentIndex - 1].slug;
}
</script>

<template>
    <div v-if="selectedStep" class="col-12 d-flex">
        <FormStepper
            v-if="formStepperConfig"
            class="col-3 d-lg-block d-none pe-2"
            :stepper-config="formStepperConfig"
        />
        <div class="col-12 col-lg-9">
            <form class="uu-form">
                <MRForm :step="selectedStep" :vuelidate="v$" />
            </form>
            <div class="btn-group">
                <NuxtLink
                    :to="{
                        name: 'procreg-slug',
                        params: { slug: getPreviousStepSlug() },
                    }"
                >
                    <BSButton variant="primary" class="btn-arrow-left">
                        {{ $t("Previous") }}
                    </BSButton>
                </NuxtLink>
                <NuxtLink
                    :to="{
                        name: 'procreg-slug',
                        params: { slug: getNextStepSlug() },
                    }"
                >
                    <BSButton variant="primary" class="btn-arrow-right">
                        {{ $t("Next") }}
                    </BSButton>
                </NuxtLink>
            </div>
        </div>
    </div>
</template>
