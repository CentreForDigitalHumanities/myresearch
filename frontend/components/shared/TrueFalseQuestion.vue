<script lang="ts" setup>
import type { TrueFalseQuestionWithValue } from "~/composables/useProcessForm";

interface Props {
    question: TrueFalseQuestionWithValue;
    isInvalid: boolean;
}

defineProps<Props>();

const modelValue = defineModel<boolean>();
</script>

<template>
    <div>
        <div class="form-check">
            <input
                :id="`${question.questionId}-${question.repeatIndex}`"
                v-model="modelValue"
                type="checkbox"
                class="form-check-input"
                :class="{ 'is-invalid': isInvalid }"
            />
            <label
                :for="`${question.questionId}-${question.repeatIndex}`"
                class="form-check-label"
            >
                {{ useTranslateableAttribute(question, "text") }}
            </label>
        </div>
        <p
            v-if="question.descriptionNl || question.descriptionEn"
            class="text-muted"
        >
            {{ useTranslateableAttribute(question, "description") }}
        </p>
    </div>
</template>
