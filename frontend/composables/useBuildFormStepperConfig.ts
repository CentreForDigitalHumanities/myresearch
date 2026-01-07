import type { FormStepperConfig } from "~/components/shared/FormStepper";
import type { QueriedForm } from "~/components/shared/FormWrapper";

/**
 * Build the configuration object required by the FormStepper component, based
 * on the queried form and current step.
 *
 * @param queriedForm The queried form data.
 * @param currentStepSlug The slug of the current step.
 * @returns The FormStepper configuration.
 */
function useBuildFormStepperConfig(
    queriedForm: QueriedForm,
    currentStepSlug: string,
): FormStepperConfig {
    return {
        steps: queriedForm.steps.map((step) => ({
            slug: step.slug,
            labelNl: step.nameNl ?? "",
            labelEn: step.nameEn ?? "",
            completed: false,
            active: step.slug === currentStepSlug,
            disabled: false,
            substeps: step.substeps.map((substep) => ({
                slug: substep.slug,
                labelNl: substep.nameNl ?? "",
                labelEn: substep.nameEn ?? "",
                completed: false,
                active: substep.slug === currentStepSlug,
                disabled: false,
                // Let's only go 2 levels deep for now.
                substeps: [],
            })),
        })),
    };
}

export { useBuildFormStepperConfig };
