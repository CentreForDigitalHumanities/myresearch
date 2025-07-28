<script lang="ts" setup>
import { ref } from "vue";
import { BSButton } from "cdh-vue-lib";
import type { FormConfig, FormStep } from "../proc-reg/types";
import FormStepper, { type FormStepperConfig } from "./FormStepper.vue";

interface Props {
  formConfig: FormConfig;
}

const props = defineProps<Props>();

const formStepperConfig = computed<FormStepperConfig>(() => {
  return {
    titleNl: props.formConfig.labelNl,
    titleEn: props.formConfig.labelEn,
    steps: props.formConfig.steps.map((step) => ({
      slug: step.slug,
      labelNl: step.stepNameNL,
      labelEn: step.stepNameEN,
      completed: false,
      active: false,
      disabled: false,
      children:
        step.substeps?.map((substep) => ({
          slug: substep.slug,
          labelNl: substep.stepNameNL,
          labelEn: substep.stepNameEN,
          completed: false,
          active: false,
          disabled: false,
          children: [],
        })) ?? [],
    })),
  };
});

const selectedStep = ref<FormStep | null>(
  props.formConfig.steps.length > 0 ? props.formConfig.steps[0] : null,
);
function nextStep(): void {
  console.log("Next step clicked");
}

function previousStep(): void {
  console.log("Previous step clicked");
}
</script>

<template>
  <div v-if="selectedStep" class="col-12 d-flex">
    <FormStepper
      class="col-2 d-lg-block d-none"
      :step-config="formStepperConfig"
      :selected-step="selectedStep.slug"
    />
    <div class="col-12 col-lg-10">
      <form class="uu-form">
        <SharedFormStep :step="selectedStep" />
      </form>
      <div class="btn-group">
        <BSButton
          variant="primary"
          class="btn-arrow-left"
          @click="() => previousStep()"
        >
          {{ $t("Previous") }}
        </BSButton>
        <BSButton
          variant="primary"
          class="btn-arrow-right"
          @click="() => nextStep()"
        >
          {{ $t("Next") }}
        </BSButton>
      </div>
    </div>
  </div>
</template>
