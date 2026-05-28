import type { UserFormInput } from "~/generated/gql/graphql";
import type {
    StepWithValues,
    SubstepWithValues,
    QuestionWithValue,
    FormWithValues,
} from "~/composables/useProcessForm";

/**
 * Recursively collects all questions from a step and its substeps, and puts them in a flat array.
 */
function getAllQuestions(
    step: StepWithValues | SubstepWithValues,
): QuestionWithValue[] {
    const ownQuestions = step.questions;

    const subStepQuestions =
        "substeps" in step
            ? (step.substeps?.flatMap(getAllQuestions) ?? [])
            : [];

    return [...ownQuestions, ...subStepQuestions];
}

/**
 * Utility function to transform our form into the expected input for our mutation.
 */
function useFormDataToMutationInput(
    formData: FormWithValues,
    submissionId: string,
): UserFormInput {
    const questions = formData.steps.flatMap(getAllQuestions);

    return {
        submissionId: submissionId,
        responses: questions.map((question) => ({
            // FileUploadQuestion answers are already the complete answer object {value, name, size}.
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
