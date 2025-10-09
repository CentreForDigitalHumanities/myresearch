<script lang="ts" setup>
import type { DateQuestionWithValue } from "~/composables/useBuildForm";

interface Props {
    question: DateQuestionWithValue;
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
            :id="question.id"
            v-model="modelValue"
            type="date"
            class="form-control"
        />
    </div>
</template>
