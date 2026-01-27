import type { QueriedForm } from "~/components/shared/FormWrapper";
import { useProcessForm } from "~/composables/useProcessForm";
import type {
    FormValidationRules,
    FormWithValues,
    StepWithValues,
    SubstepWithValues,
} from "~/composables/useProcessForm";
import type { Ref } from "vue";

interface FormState {
    formWithValues: FormWithValues | null;
    validationRules: FormValidationRules;
    formId: string | null;
}

export function useFormState(queriedFormRef: Ref<QueriedForm>) {
    const formId = queriedFormRef.value.formId;

    // useState is a cache in which values are stored globally by key.
    const formState = useState<FormState>(
        `form-state-${formId}`,
        initializeFormState,
    );

    // Reinitialize if the user navigates to a different form.
    if (formState.value.formId !== formId) {
        formState.value = initializeFormState();
    }

    function initializeFormState(): FormState {
        const processed = useProcessForm(queriedFormRef.value);
        return {
            formWithValues: processed.formWithValues,
            validationRules: processed.validationRules,
            formId,
        };
    }

    // Watch for refetches.
    watch(
        queriedFormRef,
        (newQueriedForm) => {
            const currentForm = formState.value.formWithValues;
            const processed = useProcessForm(newQueriedForm);

            // If we don't have a form yet, set it.
            // Otherwise, update the existing form with server data.
            if (!currentForm) {
                formState.value.formWithValues = processed.formWithValues;
            } else {
                reconcileForms(currentForm, processed.formWithValues);
            }
        },
        { deep: true },
    );

    return {
        formObject: computed({
            get: () => formState.value.formWithValues,
            set: (value) => {
                formState.value.formWithValues = value;
            },
        }),
        validationRules: computed(() => formState.value.validationRules),
    };
}

/**
 * Reconciles the current form with incoming form data so all nested objects
 * are updated in place, preserving reactivity.
 * 
 * For now this only updates responseIds, but if other properties of nested
 * objects (steps, questions) need to be updated based on server data, that
 * logic can be added here.
 */
function reconcileForms(
    currentForm: FormWithValues,
    incomingForm: FormWithValues,
): void {
    currentForm.steps.forEach((currentStep, stepIndex) => {
        const incomingStep = incomingForm.steps[stepIndex];
        reconcileSteps(currentStep, incomingStep);
    });
}

function reconcileSteps(
    currentStep: StepWithValues | SubstepWithValues,
    incomingStep: StepWithValues | SubstepWithValues,
): void {
    incomingStep.questions.forEach((incomingQuestion) => {
        const currentQuestion = currentStep.questions.find(
            (q) => q.questionId === incomingQuestion.questionId,
        );
        if (currentQuestion) {
            currentQuestion.responseId = incomingQuestion.responseId;
        }
    });

    if (!("substeps" in currentStep) || !("substeps" in incomingStep)) {
        return;
    }

    incomingStep.substeps?.forEach((incomingSubstep) => {
        const currentSubstep = currentStep.substeps?.find(
            (s) =>
                s.stepId === incomingSubstep.stepId &&
                s.repeatIndex === incomingSubstep.repeatIndex,
        );
        if (currentSubstep) {
            reconcileSteps(currentSubstep, incomingSubstep);
        }
    });
}
