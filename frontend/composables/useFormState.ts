import type { QueriedForm } from "~/components/form/FormWrapper";
import { useProcessForm } from "~/composables/useProcessForm";
import type {
    FormValidationRules,
    FormWithValues,
} from "~/composables/useProcessForm";
import type { Ref } from "vue";

interface FormState {
    formWithValues: FormWithValues | null;
    validationRules: FormValidationRules;
    formId: string | null;
}

export function useFormState(
    queriedFormRef: Ref<QueriedForm | null | undefined>,
) {
    const formId = computed(() => queriedFormRef.value?.formId ?? "unknown");

    // useState is a cache in which values are stored globally by key.
    const formState = useState<FormState>(
        `form-state-${formId.value}`,
        initializeFormState,
    );

    // Reinitialize if the user navigates to a different form.
    if (formState.value.formId !== formId.value) {
        formState.value = initializeFormState();
    }

    function initializeFormState(): FormState {
        const queried = queriedFormRef.value;
        if (!queried) {
            return {
                formWithValues: null,
                validationRules: { steps: [] },
                formId: null,
            };
        }
        const processed = useProcessForm(queried);
        return {
            formWithValues: processed.formWithValues,
            validationRules: processed.validationRules,
            formId: formId.value,
        };
    }

    // Reprocess form input upon refetching.
    watch(
        queriedFormRef,
        (newQueriedForm) => {
            if (!newQueriedForm) {
                return;
            }
            const processed = useProcessForm(newQueriedForm);
            formState.value.formWithValues = processed.formWithValues;
            formState.value.validationRules = processed.validationRules;
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
