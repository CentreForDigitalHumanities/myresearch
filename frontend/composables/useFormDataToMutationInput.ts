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
        responses: questions
            // Do not send questions with errors to the backend
            .filter(
                (question) => !question.errors || question.errors.length === 0,
            )
            .map((question) => ({
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
