<script lang="ts" setup>
import type { BaseQuestionInterface } from "~/generated/gql/graphql";

interface Props {
  question: Pick<
    BaseQuestionInterface,
    "questionId" | "repeatIndex" | "textNl" | "textEn" | "required"
  >;
  labelClass?: string;
}

defineProps<Props>();
</script>

<template>
  <label
    :for="`${question.questionId}-${question.repeatIndex}`"
    :class="labelClass ?? 'form-label'"
    >{{ useTranslateableAttribute(question, "text") }}
    <span v-if="question.required" class="text-danger">*</span>
  </label>
</template>
