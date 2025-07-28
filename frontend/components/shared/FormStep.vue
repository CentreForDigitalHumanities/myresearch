<script lang="ts" setup>
import type { FormStep } from "../proc-reg/types";
import FormSideBar from "./FormSideBar.vue";
import TextQuestion from "./TextQuestion.vue";
import SelectQuestion from "./SelectQuestion.vue";
import DateQuestion from "./DateQuestion.vue";

interface Props {
  step: FormStep;
}

defineProps<Props>();
</script>

<template>
  <h2>{{ useTranslateableAttribute(step, "label") }}</h2>
  <p>{{ useTranslateableAttribute(step, "description") }}</p>
  <div class="uu-form-row">
    <div class="d-flex flex-column">
      <div v-for="question in step.questions" :key="question.id">
        <TextQuestion v-if="question.type === 'text'" :question="question" />
        <SelectQuestion
          v-else-if="question.type === 'select'"
          :question="question"
        />
        <DateQuestion
          v-else-if="question.type === 'date'"
          :question="question"
        />
      </div>
    </div>
    <FormSideBar v-if="step.sideConfig" :config="step.sideConfig" />
  </div>
</template>
