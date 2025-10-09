<script lang="ts" setup>
import type { TextQuestionWithValue } from "~/composables/useBuildForm";

interface Props {
    question: TextQuestionWithValue;
}

defineProps<Props>();

const modelValue = defineModel<string>();
</script>

<template>
    <div class="uu-form-field">
        <label :for="question.id" class="form-label">{{
            useTranslateableAttribute(question, "text")
        }}</label>
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
        />
        <textarea
            v-if="question.lines && question.lines >= 2"
            :id="question.id"
            v-model="modelValue"
            class="form-control"
            :rows="question.lines"
        ></textarea>
    </div>
</template>
