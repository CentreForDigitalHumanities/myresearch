<script lang="ts" setup>
import type { FormStep } from "../proc-reg/types";
import FormSideBar from "./FormSideBar.vue";
import TextQuestion from "./TextQuestion.vue";

interface Props {
  step: FormStep;
}

const props = defineProps<Props>();
</script>

<template>
  <h2>{{ useTranslateableAttribute(step, "label") }}</h2>
  <p>{{ useTranslateableAttribute(step, "description") }}</p>
  <div v-for="question in step.questions" :key="question.id">
    <div class="uu-form-row">
      <TextQuestion v-if="question.type === 'text'" :question="question" />
      <FormSideBar v-if="step.sideConfig" :config="step.sideConfig" />
    </div>
  </div>
</template>
