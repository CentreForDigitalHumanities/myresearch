<script lang="ts" setup>
import type { NumberQuestionWithValue } from "~/composables/useProcessForm";

interface Props {
    question: NumberQuestionWithValue;
    isInvalid: boolean;
}

defineProps<Props>();

const modelValue = defineModel<number>();
</script>

<template>
    <div>
        <label :for="question.id" class="form-label">
            {{ useTranslateableAttribute(question, "text") }}
        </label>
        <p
            v-if="question.descriptionNl || question.descriptionEn"
            class="text-muted"
        >
            {{ useTranslateableAttribute(question, "description") }}
        </p>
        <input
            :id="question.id"
            v-model="modelValue"
            type="number"
            class="form-control"
            :class="{ 'is-invalid': isInvalid }"
            :min="question.positiveOnly ? 0 : undefined"
        />
    </div>
</template>
