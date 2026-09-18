import { useMutation } from "@vue/apollo-composable";
import { graphql } from "~/generated/gql";
import type { UpdateUserFormSubmission } from "~/generated/gql/graphql";
import { useNotification } from "~/composables/useNotification";
import { useI18n } from "vue-i18n";
import type { CombinedStepWithValues } from "~/composables/useProcessForm";
import useFormDataToMutationInput from "~/composables/useFormDataToMutationInput";

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

type FormSubmissionOptions = {
    reloadStudy?: boolean;
    reloadForm?: boolean;
    finalize?: boolean;
};

export function useFormSubmission(options: FormSubmissionOptions) {
    const { t } = useI18n();
    const defaultOptions = options;

    const { mutate: mutateForm } = useMutation<UpdateUserFormSubmission>(
        UPDATE_USER_FORM,
        {
            update: (cache, _, mutationOptions) => {
                const context: FormSubmissionOptions | undefined = mutationOptions.context;
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
        options?: FormSubmissionOptions,
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
                    } satisfies FormSubmissionOptions,
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