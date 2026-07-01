<script lang="ts" setup>
import type { TrueFalseQuestionWithValue } from "~/composables/useProcessForm";
import FormLabel from "../form/FormLabel.vue";

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
        <div
            v-if="question.descriptionNl || question.descriptionEn"
            class="text-muted"
            v-html="useTranslateableAttribute(question, 'description')"
        ></div>
    </div>
</template>
