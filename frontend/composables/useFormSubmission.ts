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

export function useFormSubmission(options: { reloadStudy: boolean, reloadRepeatableSteps: boolean }) {
    const { t } = useI18n();

    const { mutate: mutateForm } = useMutation<UpdateUserFormSubmission>(
        UPDATE_USER_FORM,
        {
            update: (cache) => {
                cache.evict({ fieldName: "form" });
                if (options.reloadStudy) {
                    cache.evict({ fieldName: "study" });
                }
                if (options.reloadRepeatableSteps) {
                    cache.evict({ fieldName: "repeatableStepsWithRepeats" });
                }
                cache.gc();
            },
        },
    );

    async function submitForm(
        step: CombinedStepWithValues,
        submissionId: string,
        finalize: boolean = false,
    ) {
        const inputData = useFormDataToMutationInput(step, submissionId);

        try {
            await mutateForm({
                userFormInput: inputData,
                finalize,
            });
        } catch {
            useNotification(
                t("An error occurred while saving the form. Please try again."),
                "danger",
            );
        }
    }

    return { submitForm };
}