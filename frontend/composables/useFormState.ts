import type { QueriedForm } from "~/components/shared/FormWrapper";
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

  // Reprocess form input upon refetching.
  watch(
    queriedFormRef,
    (newQueriedForm) => {
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
