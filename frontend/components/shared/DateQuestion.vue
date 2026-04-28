<script lang="ts" setup>
import type { DateQuestionWithValue } from "~/composables/useProcessForm";
import FormLabel from "./FormLabel.vue";

interface Props {
    question: DateQuestionWithValue;
    isInvalid: boolean;
}

defineProps<Props>();

const modelValue = defineModel<string>();
</script>

<template>
    <div>
        <FormLabel :question="question" />
        <div
            v-if="question.descriptionNl || question.descriptionEn"
            class="text-muted"
            v-html="useTranslateableAttribute(question, 'description')"
        ></div>
        <input
            :id="`${question.questionId}-${question.repeatIndex}`"
            v-model="modelValue"
            type="date"
            class="form-control"
            :class="{ 'is-invalid': isInvalid }"
        />
    </div>
</template>
