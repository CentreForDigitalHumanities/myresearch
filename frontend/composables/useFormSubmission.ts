import { useMutation } from "@vue/apollo-composable";
import { graphql } from "~/generated/gql";
import type { UpdateUserFormSubmission } from "~/generated/gql/graphql";
import { useNotification } from "~/composables/useNotification";
import { useI18n } from "vue-i18n";
import type { CombinedStepWithValues } from "~/composables/useProcessForm";

const UPDATE_USER_FORM = graphql(`
    mutation SaveFormSubmission(
        $userFormInput: UserFormInput!
        $finalize: Boolean
    ) {
        updateFormSubmission(
            userFormInput: $userFormInput
            finalize: $finalize
        ) {
            ok
            errors {
                field
                messages
            }
        }
    }
`);

export function useFormSubmission(options: { reloadStudy: boolean, reloadForm: boolean }) {
    const { t } = useI18n();
    const defaultOptions = options;

    const { mutate: mutateForm } = useMutation<UpdateUserFormSubmission>(
        UPDATE_USER_FORM,
        {
            update: (cache, _, mutationOptions) => {
                const context = mutationOptions.context as { reloadForm?: boolean; reloadStudy?: boolean } | undefined;
                if (context?.reloadForm ?? defaultOptions.reloadForm) {
                    cache.evict({ fieldName: "form" });
                }
                if (context?.reloadStudy ?? defaultOptions.reloadStudy) {
                    cache.evict({ fieldName: "study" });
                }
                cache.evict({ fieldName: "repeatableStepsWithRepeats" });
                cache.gc();
            },
        },
    );

    async function submitForm(
        step: CombinedStepWithValues,
        submissionId: string,
        options?: { finalize?: boolean; reloadForm?: boolean; reloadStudy?: boolean },
    ) {
        const inputData = useFormDataToMutationInput(step, submissionId);

        try {
            await mutateForm(
                {
                    userFormInput: inputData,
                    finalize: options?.finalize ?? false,
                },
                {
                    context: {
                        reloadForm: options?.reloadForm ?? true,
                        reloadStudy: options?.reloadStudy ?? false,
                    },
                },
            );
        } catch {
            useNotification(
                t("An error occurred while saving the form. Please try again."),
                "danger",
            );
        }
    }

    return { submitForm };
}