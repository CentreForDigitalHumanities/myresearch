<script lang="ts" setup>
import { ref, computed } from "vue";
import { BSButton } from "cdh-vue-lib";
import type { FormConfig, FormStep } from "../form/types";
import FormStepper, { type FormStepperConfig } from "./FormStepper.vue";

interface Props {
  formConfig: FormConfig;
  currentStepSlug: string;
}

const props = defineProps<Props>();

const formStepperConfig = computed<FormStepperConfig>(() => {
    const selectedStepSlug = selectedStep.value?.slug;

    return {
        titleNl: props.formConfig.labelNl,
        titleEn: props.formConfig.labelEn,
        steps: props.formConfig.steps.map((step) => ({
            slug: step.slug,
            labelNl: step.stepNameNL,
            labelEn: step.stepNameEN,
            completed: false,
            active: step.slug === selectedStepSlug,
            disabled: false,
            children:
                step.substeps?.map((substep) => ({
                    slug: substep.slug,
                    labelNl: substep.stepNameNL,
                    labelEn: substep.stepNameEN,
                    completed: false,
                    active: substep.slug === selectedStepSlug,
                    disabled: false,
                    children: [],
                })) ?? [],
        })),
    };
});

const selectedStep = ref<FormStep | null>(
  props.formConfig.steps.length > 0 ? getAllSteps().find(({ slug }) => slug === props.currentStepSlug) ?? null : null,
);

function getAllSteps(): FormStep[] {
    const allSteps: FormStep[] = [];

    props.formConfig.steps.forEach((step) => {
        // Add main step.
        allSteps.push(step);

        if (!step.substeps || step.substeps.length === 0) {
            return;
        }

        // Add substeps sorted by order.
        const sortedSubsteps = [...step.substeps].sort(
            (a, b) => a.order - b.order,
        );
        allSteps.push(...sortedSubsteps);
    });

    return allSteps;
}

function findCurrentStepIndex(): number {
    const selectedStepValue = selectedStep.value;
    if (!selectedStepValue) {
        return -1;
    }

    const allSteps = getAllSteps();
    return allSteps.findIndex((step) => step.slug === selectedStepValue.slug);
}

function getNextStepSlug(): string {
  if (!selectedStep.value) {
    return props.currentStepSlug;
  }

    const allSteps = getAllSteps();
    const currentIndex = findCurrentStepIndex();

  if (currentIndex === -1 || currentIndex >= allSteps.length - 1) {
    // Already at the last step or step not found.
    return props.currentStepSlug;
  }

  return allSteps[currentIndex + 1].slug
}

function getPreviousStepSlug(): string {
  if (!selectedStep.value) {
    return props.currentStepSlug;
  }

    const allSteps = getAllSteps();
    const currentIndex = findCurrentStepIndex();

  if (currentIndex <= 0) {
    // Already at the first step or step not found.
    return props.currentStepSlug;
  }

  return allSteps[currentIndex - 1].slug;
}
</script>

<template>
  <div v-if="selectedStep" class="col-12 d-flex">
    <FormStepper
      class="col-2 d-lg-block d-none"
      :step-config="formStepperConfig"
      :selected-step="props.currentStepSlug"
    />
    <div class="col-12 col-lg-10">
      <form class="uu-form">
        <SharedFormStep :step="selectedStep" />
      </form>
      <div class="btn-group">
        <NuxtLink :to="{ name: 'procreg-step', params: { step: getPreviousStepSlug() } }">
          <BSButton
            variant="primary"
            class="btn-arrow-left"
          >
            {{ $t("Previous") }}
          </BSButton>
        </NuxtLink>
        <NuxtLink :to="{ name: 'procreg-step', params: { step: getNextStepSlug() } }">
          <BSButton
            variant="primary"
            class="btn-arrow-right"
          >
            {{ $t("Next") }}
          </BSButton>
        </NuxtLink>
      </div>
    </div>
  </div>
</template>
