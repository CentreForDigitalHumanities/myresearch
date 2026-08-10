import { graphql } from "~/generated/gql";
import type { UpdateUserFormSubmission } from "~/generated/gql/graphql";
import { useMutation } from "@vue/apollo-composable";

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

export function useUpdateFormSubmission(reloadStudy: boolean = false) {
    const { mutate: mutateForm } = useMutation<UpdateUserFormSubmission>(
        UPDATE_USER_FORM,
        {
            update: (cache) => {
                cache.evict({ fieldName: "form" });
                if (reloadStudy) {
                    cache.evict({ fieldName: "study" });
                }
                cache.gc();
            },
        },
    );

    return {
        mutateForm,
    };
}
