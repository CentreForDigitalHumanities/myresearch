<script lang="ts" setup>
import { useTranslateableAttribute } from "~/composables/useTranslation";

interface FormStep {
  slug: string;
  labelNl: string;
  labelEn: string;
  children: FormStep[];
  completed: boolean;
  active: boolean;
  disabled: boolean;
}

export interface FormStepperConfig {
  titleNl?: string;
  titleEn?: string;
  steps: Array<FormStep>;
}

interface Props {
  selectedStep: string;
  stepConfig: FormStepperConfig;
}

const props = defineProps<Props>();

function stepperItemClasses(step: FormStep): string {
  const classes: string[] = ["stepper-item"];
  if (step.active) {
    classes.push("active");
  }
  if (step.completed) {
    classes.push("complete");
  }
  if (step.disabled) {
    classes.push("disabled");
  }
  return classes.join(" ");
}
</script>

<template>
  <div class="stepper">
    <p class="mb-4">
      {{ useTranslateableAttribute(props.stepConfig, "title") }}
    </p>
    <ul>
      <li v-for="(step, index) in props.stepConfig.steps" :key="index">
        <a :class="stepperItemClasses(step)">
          <span class="stepper-bubble stepper-bubble-largest">{{
            index + 1
          }}</span>
          <span>{{ useTranslateableAttribute(step, "label") }}</span>
        </a>
        <ul v-if="step.children.length > 0">
          <li v-for="(child, childIndex) in step.children" :key="childIndex">
            <a :class="stepperItemClasses(child)">
              <span class="stepper-bubble stepper-bubble-medium"></span>
              <span>{{ useTranslateableAttribute(child, "label") }}</span>
            </a>
          </li>
        </ul>
      </li>
    </ul>
  </div>
</template>
