import type { ErrorObject, Validation } from "@vuelidate/core";

/**
 * Creates a flat map of form questions and errors, and then marks the steps
 * and substeps that contain questions with errors as such.
 *
 * This only traverses the form once.
 */
export function useAnnotateErrors(
    vuelidate: Validation,
    form: FormWithValues,
): void {
    const errorsByPath = new Map<string, ErrorObject[]>();
    vuelidate.$errors.forEach((error) => {
        const existing = errorsByPath.get(error.$propertyPath);
        if (existing) {
            existing.push(error);
        } else {
            errorsByPath.set(error.$propertyPath, [error]);
        }
    });

    form.steps.forEach((step) => {
        let stepHasErrors = false;

        step.questions.forEach((question) => {
            // combined with autodirty from v$ in FormWrapper.vue this creates the warnings on the form.
            question.errors = errorsByPath.get(question.location) ?? [];
            stepHasErrors = stepHasErrors || question.errors.length > 0;
        });

        step.substeps?.forEach((subStep) => {
            subStep.questions.forEach((question) => {
                question.errors = errorsByPath.get(question.location) ?? [];
            });
            subStep.hasErrors = subStep.questions.some(
                (q) => (q.errors?.length ?? 0) > 0,
            );
            stepHasErrors = stepHasErrors || subStep.hasErrors;
        });

        step.hasErrors = stepHasErrors;
    });
}
