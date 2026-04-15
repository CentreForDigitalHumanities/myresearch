import type { FormStep, FormStepperConfig } from "~/components/form/FormStepper";
import type { QueriedForm } from "~/components/form/FormWrapper";
import { useOverviewStepSlug } from "./useOverviewStepSlug";

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
    const steps: FormStep[] = queriedForm.steps.map((step) => ({
        slug: step.slug,
        labelNl: step.nameNl,
        labelEn: step.nameEn,
        completed: false,
        active: step.slug === currentStepSlug,
        disabled: false,
        substeps: step.substeps.map((substep) => ({
            slug: substep.slug,
            labelNl: substep.nameNl,
            labelEn: substep.nameEn,
            completed: false,
            active: substep.slug === currentStepSlug,
            disabled: false,
            // Let's only go 2 levels deep for now.
            substeps: [],
        })),
    }));

    const overviewStepSlug = useOverviewStepSlug();

    steps.push({
        slug: overviewStepSlug,
        labelNl: "Overzicht",
        labelEn: "Overview",
        completed: false,
        active: currentStepSlug === overviewStepSlug,
        disabled: false,
        substeps: [],
    });

    return { steps };
}

export { useBuildFormStepperConfig };
