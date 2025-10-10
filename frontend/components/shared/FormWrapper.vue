<script lang="ts" setup>
import { computed } from "vue";
import { BSButton } from "cdh-vue-lib";
import type { QueriedForm } from "./FormWrapper";
import FormStepper, { type FormStepperConfig } from "./FormStepper";
import MRForm from "./MRForm.vue";
import { useBuildFormStepperConfig } from "~/composables/useBuildFormStepperConfig";
import useVuelidate from "@vuelidate/core";

interface Props {
    queriedForm: QueriedForm;
    currentStepSlug: string;
}
const props = defineProps<Props>();

const formArtifacts = computed(() => reactive(useBuildForm(props.queriedForm)));

const formObject = computed(() => formArtifacts.value.formWithValues);
const validationRules = computed(() => formArtifacts.value.validationRules);

const v$ = useVuelidate(validationRules, formObject, {
    $autoDirty: true,
});

// Stepper configuration
const formStepperConfig = computed<FormStepperConfig | null>(() =>
    useBuildFormStepperConfig(props.queriedForm, props.currentStepSlug),
);

const allSteps = computed(() => getAllSteps(formObject.value));
const selectedStep = computed(() => {
    const steps = allSteps.value;
    if (steps.length <= 0) {
        return null;
    }
    return steps.find(({ slug }) => slug === props.currentStepSlug) ?? null;
});

function getAllSteps(form: FormWithValues): CombinedStepWithValues[] {
    return form.steps.flatMap((step) => {
        const steps: CombinedStepWithValues[] = [step];
        if ("substeps" in step) {
            const substeps = step.substeps;
            if (substeps) {
                steps.push(...substeps);
            }
        }
        return steps;
    });
}

function findCurrentStepIndex(): number {
    const selectedStepValue = selectedStep.value;
    if (!selectedStepValue) {
        return -1;
    }

    const steps = allSteps.value;
    return steps.findIndex((step) => step.slug === selectedStepValue.slug);
}

function getNextStepSlug(): string {
    if (!selectedStep.value) {
        return props.currentStepSlug;
    }

    const steps = allSteps.value;
    const currentIndex = findCurrentStepIndex();

    if (currentIndex === -1 || currentIndex >= steps.length - 1) {
        // Already at the last step or step not found.
        return props.currentStepSlug;
    }

    return steps[currentIndex + 1].slug;
}

function getPreviousStepSlug(): string {
    if (!selectedStep.value) {
        return props.currentStepSlug;
    }

    const steps = allSteps.value;
    const currentIndex = findCurrentStepIndex();

    if (currentIndex <= 0) {
        // Already at the first step or step not found.
        return props.currentStepSlug;
    }

    return steps[currentIndex - 1].slug;
}
</script>

<template>
    <div v-if="selectedStep" class="col-12 d-flex">
        <FormStepper
            v-if="formStepperConfig"
            class="col-3 d-lg-block d-none pe-2"
            :stepper-config="formStepperConfig"
        />
        <div class="col-12 col-lg-9">
            <form class="uu-form">
                <MRForm :step="selectedStep" :vuelidate="v$" />
            </form>
            <div class="btn-group">
                <NuxtLink
                    :to="{
                        name: 'procreg-slug',
                        params: { slug: getPreviousStepSlug() },
                    }"
                >
                    <BSButton variant="primary" class="btn-arrow-left">
                        {{ $t("Previous") }}
                    </BSButton>
                </NuxtLink>
                <NuxtLink
                    :to="{
                        name: 'procreg-slug',
                        params: { slug: getNextStepSlug() },
                    }"
                >
                    <BSButton variant="primary" class="btn-arrow-right">
                        {{ $t("Next") }}
                    </BSButton>
                </NuxtLink>
            </div>
        </div>
    </div>
</template>
