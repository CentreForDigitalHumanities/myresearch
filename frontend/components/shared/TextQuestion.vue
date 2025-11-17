<script lang="ts" setup>
import type { TextQuestionWithValue } from "~/composables/useProcessForm";

interface Props {
    question: TextQuestionWithValue;
    isInvalid: boolean;
}

defineProps<Props>();

const modelValue = defineModel<string>();
</script>

<template>
    <div>
        <label :for="question.id" class="form-label"
            >{{ useTranslateableAttribute(question, "text") }}
        </label>
        <p
            v-if="question.descriptionNl || question.descriptionEn"
            class="text-muted"
        >
            {{ useTranslateableAttribute(question, "description") }}
        </p>
        <input
            v-if="!question.lines || question.lines < 2"
            :id="question.id"
            v-model="modelValue"
            type="text"
            class="form-control"
            :class="{ 'is-invalid': isInvalid }"
        />
        <textarea
            v-if="question.lines && question.lines >= 2"
            :id="question.id"
            v-model="modelValue"
            class="form-control"
            :class="{ 'is-invalid': isInvalid }"
            :rows="question.lines"
        ></textarea>
    </div>
</template>
