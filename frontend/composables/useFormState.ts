import type { QueriedForm } from "~/components/shared/FormWrapper";
import { useProcessForm } from "~/composables/useProcessForm";
import type {
    FormValidationRules,
    FormWithValues,
} from "~/composables/useProcessForm";

interface FormState {
    formWithValues: FormWithValues | null;
    validationRules: FormValidationRules;
    formId: string | null;
}

/**
 * Composable to persist form state across navigation.
 * This ensures that form values are not lost when switching between steps.
 */
export function useFormState(queriedForm: QueriedForm) {
    // Use the form's unique identifier as the state key
    const formId = queriedForm.formId;

    // useState is a cache in which values are stored globally by key.
    // If a value already exists for the given key, it is returned.
    // If not, the initializer function is called to create the value.
    const formState = useState<FormState>(
        `form-state-${formId}`,
        initializeFormState,
    );

    // Reinitialize formState if the form ID has changed
    // (e.g. when the user navigates to a different form).
    if (formState.value.formId !== formId) {
        formState.value = initializeFormState();
    }

    function initializeFormState(): FormState {
        const processed = useProcessForm(queriedForm);
        return {
            formWithValues: processed.formWithValues,
            validationRules: processed.validationRules,
            formId,
        };
    }

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
