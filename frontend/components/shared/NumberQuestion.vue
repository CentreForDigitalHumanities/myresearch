<script lang="ts" setup>
import type { NumberQuestionWithValue } from "~/composables/useProcessForm";
import FormLabel from "./FormLabel.vue";

interface Props {
  question: NumberQuestionWithValue;
  isInvalid: boolean;
}

defineProps<Props>();

const modelValue = defineModel<number>();
</script>

<template>
  <div>
    <FormLabel :question="question" />
    <p
      v-if="question.descriptionNl || question.descriptionEn"
      class="text-muted"
    >
      {{ useTranslateableAttribute(question, "description") }}
    </p>
    <input
      :id="`${question.questionId}-${question.repeatIndex}`"
      v-model="modelValue"
      type="number"
      class="form-control"
      :class="{ 'is-invalid': isInvalid }"
      :min="question.positiveOnly ? 0 : undefined"
    />
  </div>
</template>
