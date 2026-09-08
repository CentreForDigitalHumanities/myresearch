<script lang="ts" setup>
import { computed } from "vue";
import { BSButton, useConfirm } from "cdh-vue-lib";
import type { QueriedForm } from "./FormWrapper";
import FormStepper, { type FormStepperConfig } from "./FormStepper";
import FormSideBar from "../form/FormSideBar.vue";
import MRForm from "~/components/form/MRForm.vue";
import { useBuildFormStepperConfig } from "~/composables/useBuildFormStepperConfig";
import { useFormState } from "~/composables/useFormState";
import { useFormSubmission } from "~/composables/useFormSubmission";
import useVuelidate from "@vuelidate/core";
import { useStudyId } from "~/composables/useRouteParams";
import SubmissionOverview from "~/components/form/overview/OverviewForm.vue";
import { useI18n } from "vue-i18n";
import { Send, TriangleAlert, MoveLeft } from "lucide-vue-next";
import { useAnnotateErrors } from "~/composables/useAnnotateErrors";
import { useNotification } from "~/composables/useNotification";

interface Props {
    queriedForm: QueriedForm;
    currentStepSlug: string;
    reloadStudy: boolean;
}
const props = defineProps<Props>();

const queried = computed(() => props.queriedForm);
const { formObject, validationRules } = useFormState(queried);

const studyId = useStudyId();
const { t } = useI18n();

const v$ = useVuelidate(
    validationRules,
    computed(() => formObject.value ?? { steps: [] }),
    {
        $autoDirty: true,
    },
);

const { submitForm: mutateFormSubmission } = useFormSubmission({
    reloadStudy: props.reloadStudy,
});

function submitForm(options = { submit: false }): void {
    const formData = formObject.value;
    if (!formData) {
        return;
    }

    if (options.submit) {
        void v$.value.$validate();
        if (v$.value.$invalid) {
            return;
        }
    }

    const step = selectedStep.value;
    if (!step) {
        return;
    }

    void mutateFormSubmission(
        step,
        props.queriedForm.submissionId,
        options.submit,
    ).then(() => {
        if (options.submit) {
            useNotification(
                t("Registration submitted successfully."),
                "success",
            );
            void navigateTo({
                name: "studies-studyId",
                params: {
                    studyId: studyId.value,
                },
            });
        }
    });
}

function finalSubmit(): void {
    useConfirm({
        headerText: t("Confirm submission"),
        text: t(
            "Are you sure you want to submit the form? Once submitted, you will not be able to make changes.",
        ),
        confirmText: t("Yes"),
        abortText: t("No"),
        callback: () => {
            submitForm({ submit: true });
        },
    });
}

// Annotate form objects with validation errors whenever they change.
watchEffect(() => {
    if (formObject.value) {
        useAnnotateErrors(v$.value, formObject.value);
    }
});

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

const showSubmissionWarning = computed(
    // If we are on the overview step, but we have validation errors, show a warning
    () => !!(selectedStep.value?.isOverview && v$.value.$invalid),
);

watchEffect(() => {
    if (formObject.value && showSubmissionWarning.value) {
        void v$.value.$validate();
        useAnnotateErrors(v$.value, formObject.value);
    }
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

    const id = studyId.value;
    if (!id) {
        return;
    }

    return navigateTo({
        name: "studies-studyId-submissionId-slug",
        params: {
            studyId: id,
            submissionId: props.queriedForm.submissionId,
            slug: slug,
        },
    });
}

function handleBackNavigation() {
    submitForm();
    useNotification(t("Your progress has been saved."), "info", 3);

    return navigateTo({
        name: "studies-studyId",
        params: { studyId: studyId.value },
    });
}
</script>

<template>
    <div class="mb-3">
        <a href="#" class="pe-auto" @click.prevent="handleBackNavigation">
            <div class="d-flex gap-2 align-items-center">
                <MoveLeft class="icon" />
                <div class="ml-3">{{ t("Save and go back") }}</div>
            </div>
        </a>
    </div>
    <div v-if="selectedStep" class="col-12 d-flex">
        <FormStepper
            v-if="formStepperConfig"
            class="col-3 d-lg-block d-none pe-2"
            :stepper-config="formStepperConfig"
            @step-clicked="navigateToSlug"
        />
        <div v-if="selectedStep.isOverview && formObject" class="col-9">
            <SubmissionOverview :form="formObject" />
            <div class="mb-3">
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
            </div>
            <div class="btn-group">
                <BSButton
                    variant="primary"
                    class="btn-arrow-left"
                    @click="navigateToSlug(getPreviousStepSlug())"
                >
                    {{ $t("Previous") }}
                </BSButton>
                <BSButton
                    v-if="selectedStep.isOverview"
                    :disabled="showSubmissionWarning"
                    :variant="showSubmissionWarning ? 'light' : 'success'"
                    @click="showSubmissionWarning ? undefined : finalSubmit"
                >
                    {{ $t("Submit") }}
                    <Send class="ms-2" :size="16" />
                </BSButton>
            </div>
        </div>
        <template v-else>
            <div class="col-12 col-lg-6 pe-4">
                <form class="uu-form uu-form-no-help">
                    <h2>
                        {{ useTranslateableAttribute(selectedStep, "name") }}
                    </h2>
                    <div
                        v-html="
                            useTranslateableAttribute(
                                selectedStep,
                                'description',
                            )
                        "
                    ></div>
                    <MRForm
                        :step="selectedStep"
                        @repeat-step-clicked="navigateToSlug"
                    />
                </form>
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
                        variant="primary"
                        class="btn-arrow-right"
                        @click="navigateToSlug(getNextStepSlug())"
                    >
                        {{ $t("Next") }}
                    </BSButton>
                </div>
            </div>
            <div class="col-3 d-lg-block d-none">
                <FormSideBar :step="selectedStep" />
            </div>
        </template>
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
