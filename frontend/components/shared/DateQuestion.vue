<script lang="ts" setup>
import type { DateQuestionWithValue } from "~/composables/useProcessForm";

interface Props {
    question: DateQuestionWithValue;
    isInvalid: boolean;
}

defineProps<Props>();

const modelValue = defineModel<string>();
</script>

<template>
    <div>
        <label :for="`${question.questionId}-${question.repeatIndex}`" class="form-label">
            {{ useTranslateableAttribute(question, "text") }}
        </label>
        <p
            v-if="question.descriptionNl || question.descriptionEn"
            class="text-muted"
        >
            {{ useTranslateableAttribute(question, "description") }}
        </p>
        <input
            :id="`${question.questionId}-${question.repeatIndex}`"
            v-model="modelValue"
            type="date"
            class="form-control"
            :class="{ 'is-invalid': isInvalid }"
        />
    </div>
</template>
