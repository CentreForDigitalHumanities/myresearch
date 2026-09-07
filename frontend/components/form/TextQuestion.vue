<script lang="ts" setup>
import type { TextQuestionWithValue } from "~/composables/useProcessForm";
import FormLabel from "../form/FormLabel.vue";

interface Props {
    question: TextQuestionWithValue;
    isInvalid: boolean;
    isFirstRepeat?: boolean;
}

const props = defineProps<Props>();

const modelValue = defineModel<string>();
</script>

<template>
    <div>
        <FormLabel :question="question" />
        <template v-if="props.isFirstRepeat">
            <div
                v-if="question.descriptionNl || question.descriptionEn"
                class="text-muted"
                v-html="useTranslateableAttribute(question, 'description')"
            ></div>
        </template>
        <input
            v-if="!question.lines || question.lines < 2"
            :id="`${question.questionId}-${question.repeatIndex}`"
            v-model="modelValue"
            type="text"
            class="form-control"
            :class="{ 'is-invalid': isInvalid }"
        />
        <textarea
            v-if="question.lines && question.lines >= 2"
            :id="`${question.questionId}-${question.repeatIndex}`"
            v-model="modelValue"
            class="form-control"
            :class="{ 'is-invalid': isInvalid }"
            :rows="question.lines"
        ></textarea>
    </div>
</template>
