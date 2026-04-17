<script lang="ts" setup>
import { computed } from "vue";
import { BSButton } from "cdh-vue-lib";
import type { QueriedForm } from "./FormWrapper";
import FormStepper, { type FormStepperConfig } from "./FormStepper";
import MRForm from "~/components/form/MRForm.vue";
import { useBuildFormStepperConfig } from "~/composables/useBuildFormStepperConfig";
import { useFormState } from "~/composables/useFormState";
import useVuelidate from "@vuelidate/core";
import { graphql } from "~/generated/gql";
import type { UpdateUserFormSubmission } from "~/generated/gql/graphql";
import { useMutation } from "@vue/apollo-composable";
import SubmissionOverview from "~/components/form/overview/OverviewForm.vue";
import { useI18n } from "vue-i18n";
import { Send, TriangleAlert } from "lucide-vue-next";

interface Props {
    queriedForm: QueriedForm;
    currentStepSlug: string;
}
const props = defineProps<Props>();

const queried = computed(() => props.queriedForm);
const { formObject, validationRules } = useFormState(queried);

const { t } = useI18n();

const showSubmissionWarning = ref(false);

const UPDATE_USER_FORM = graphql(`
    mutation SaveFormSubmission(
        $submissionId: ID!
        $responses: [ResponseInput!]!
    ) {
        updateFormSubmission(
            userFormInput: {
                submissionId: $submissionId
                responses: $responses
            }
        ) {
            ok
            errors {
                field
                messages
            }
        }
    }
`);

const { mutate: mutateForm } = useMutation<UpdateUserFormSubmission>(
    UPDATE_USER_FORM,
    {
        update: (cache) => {
            cache.evict({ fieldName: "form" });
            cache.gc();
        },
    },
);

function submitForm(options = { submit: false }): void {
    const formData = formObject.value;
    if (!formData) {
        return;
    }

    if (options.submit) {
        void v$.value.$validate();
        if (v$.value.$invalid) {
            showSubmissionWarning.value = true;
            return;
        }
    }

    const inputData = useFormDataToMutationInput(
        formData,
        props.queriedForm.submissionId,
    );

    void mutateForm(inputData)
        .catch(() => {
            useNotification(
                t("An error occurred while saving the form. Please try again."),
                "danger",
            );
        })
        .then(() => {
            if (options.submit) {
                // TODO: navigate to the study detail page.
                useNotification(
                    t("Registration submitted successfully."),
                    "success",
                );
            }
        });
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

const firstStepSelected = computed(() => {
    const selected = selectedStep.value;
    if (!selected) {
        return false;
    }
    const steps = allSteps.value;
    return steps[0].slug === selected.slug;
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

/**
 * Funnel for navigation events from the stepper and navigation buttons.
 * Submits the form as a side effect and then navigates to the provided slug.
 * This is also where navigation can be blocked if there are validation errors.
 */
function navigateToSlug(slug: string) {
    submitForm();
    return navigateTo(
        "/procreg/" + props.queriedForm.submissionId + "/" + slug,
    );
}
</script>

<template>
    <div v-if="selectedStep" class="col-12 d-flex">
        <FormStepper
            v-if="formStepperConfig"
            class="col-3 d-lg-block d-none pe-2"
            :stepper-config="formStepperConfig"
            @step-clicked="navigateToSlug"
        />
        <div class="col-12 col-lg-9">
            <form class="uu-form">
                <SubmissionOverview
                    v-if="selectedStep.isOverview && formObject"
                    :form="formObject"
                />
                <MRForm
                    v-else
                    :step="selectedStep"
                    :vuelidate="v$"
                    @submit-form="submitForm"
                />
            </form>

            <div class="mb-3">
                <Transition name="fade">
                    <div
                        v-if="showSubmissionWarning"
                        class="alert alert-warning d-inline-flex align-items-center gap-2"
                        role="alert"
                    >
                        <TriangleAlert class="icon" />
                        <span>
                            {{
                                t(
                                    "Your form contains errors. Please review and resubmit.",
                                )
                            }}
                        </span>
                    </div>
                </Transition>
            </div>

            <div class="btn-group">
                <BSButton
                    v-if="!firstStepSelected"
                    variant="primary"
                    class="btn-arrow-left"
                    @click="navigateToSlug(getPreviousStepSlug())"
                >
                    {{ $t("Previous") }}
                </BSButton>
                <BSButton
                    v-if="selectedStep.isOverview"
                    variant="success"
                    @click="submitForm({ submit: true })"
                >
                    {{ $t("Submit") }}
                    <Send class="ms-2" :size="16" />
                </BSButton>
                <BSButton
                    v-else
                    variant="primary"
                    class="btn-arrow-right"
                    @click="navigateToSlug(getNextStepSlug())"
                >
                    {{ $t("Next") }}
                </BSButton>
            </div>
        </div>
    </div>
</template>

<style lang="scss" scoped>
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}
</style>
