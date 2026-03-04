<script lang="ts" setup>
import type { TrueFalseQuestionWithValue } from "~/composables/useProcessForm";
import FormLabel from "./FormLabel.vue";

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
            <FormLabel :question="question" label-class="form-check-label" />
        </div>
        <p
            v-if="question.descriptionNl || question.descriptionEn"
            class="text-muted"
        >
            {{ useTranslateableAttribute(question, "description") }}
        </p>
    </div>
</template>
