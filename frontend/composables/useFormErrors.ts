import type { ErrorObject, Validation } from "@vuelidate/core";

/**
 * Get validation errors for a specific question.
 */
export function useGetQuestionErrors(
    vuelidate: Validation,
    question: QuestionWithValue,
): ErrorObject[] {
    return vuelidate.$errors.filter(
        (error) => error.$propertyPath === question.location,
    );
}

/**
 * Check if a specific question has validation errors.
 */
export function useQuestionHasErrors(
    vuelidate: Validation,
    question: QuestionWithValue,
): boolean {
    return useGetQuestionErrors(vuelidate, question).length > 0;
}

/**
 * Check if a step or any of its substeps have any invalid questions
 * Uses trampolining (iteration instead of recursion) to process nested substeps
 */
export function useStepHasErrors(
    vuelidate: Validation,
    step: CombinedStepWithValues,
): boolean {
    // Trampolining approach: use a stack to iteratively process steps and substeps
    const stepsToCheck: CombinedStepWithValues[] = [step];

    while (stepsToCheck.length > 0) {
        const currentStep = stepsToCheck.pop();

        // This is just to satisfy the type checker.
        if (!currentStep) {
            continue;
        }

        if (
            currentStep.questions.some((question) =>
                useQuestionHasErrors(vuelidate, question),
            )
        ) {
            return true;
        }

        // Add substeps to the stack if they exist.
        if ("substeps" in currentStep && currentStep.substeps) {
            stepsToCheck.push(...currentStep.substeps);
        }
    }

    return false;
}
