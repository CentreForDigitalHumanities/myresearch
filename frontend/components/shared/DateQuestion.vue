<script lang="ts" setup>
import type { DateQuestion } from "../form/types";

interface Props {
  question: DateQuestion;
}

defineProps<Props>();
</script>

<template>
  <div class="uu-form-field">
    <label :for="question.id" class="form-label">{{
      useTranslateableAttribute(question, "label")
    }}</label>
    <p
      v-if="question.descriptionNl || question.descriptionEn"
      class="text-muted"
    >
      {{ useTranslateableAttribute(question, "description") }}
    </p>
    <input :id="question.id" type="date" class="form-control" />
  </div>
</template>
