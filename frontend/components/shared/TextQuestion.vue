<script lang="ts" setup>
import type { TextQuestion } from "../proc-reg/types";

interface Props {
  question: TextQuestion;
}

const props = defineProps<Props>();
</script>

<template>
  <div class="uu-form-field">
    <label :for="question.id" class="form-label">{{
      useTranslateableAttribute(question, "label")
    }}</label>
    <p>{{ useTranslateableAttribute(question, "description") }}</p>
    <input :id="question.id" type="text" class="form-control" />
  </div>
</template>
