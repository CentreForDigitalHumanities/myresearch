import type { UserFormInput } from "~/generated/gql/graphql";
import type { CombinedStepWithValues } from "~/composables/useProcessForm";

/**
 * Utility function to transform the responses of a single step (or substep)
 * into the expected input for our mutation.
 */
function useFormDataToMutationInput(
    step: CombinedStepWithValues,
    submissionId: string,
): UserFormInput {
    const questions = step.questions;

    return {
        submissionId: submissionId,
        responses: questions.map((question) => ({
            // FileUploadQuestion answers are already in the correct format.
            answer:
                question.__typename === "FileUploadQuestionType"
                    ? JSON.stringify(question.value ?? { value: "" })
                    : JSON.stringify({ value: question.value }),
            id: question.responseId,
            questionId: question.questionId,
            repeatIndex: question.repeatIndex,
        })),
    };
}

export default useFormDataToMutationInput;
