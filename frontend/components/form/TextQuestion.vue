<script lang="ts" setup>
import type { TextQuestionWithValue } from "~/composables/useProcessForm";
import FormLabel from "../form/FormLabel.vue";

interface Props {
    question: TextQuestionWithValue;
    isInvalid: boolean;
}

defineProps<Props>();

const modelValue = defineModel<string>();

const emit = defineEmits<{
    blur: [];
}>();
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
            v-if="!question.lines || question.lines < 2"
            :id="`${question.questionId}-${question.repeatIndex}`"
            v-model="modelValue"
            type="text"
            class="form-control"
            :class="{ 'is-invalid': isInvalid }"
            @blur="emit('blur')"
        />
        <textarea
            v-if="question.lines && question.lines >= 2"
            :id="`${question.questionId}-${question.repeatIndex}`"
            v-model="modelValue"
            class="form-control"
            :class="{ 'is-invalid': isInvalid }"
            :rows="question.lines"
            @blur="emit('blur')"
        ></textarea>
    </div>
</template>
