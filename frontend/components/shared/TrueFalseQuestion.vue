<script lang="ts" setup>
import type { TrueFalseQuestionWithValue } from "~/composables/useBuildForm";

interface Props {
    question: TrueFalseQuestionWithValue;
}

defineProps<Props>();

const modelValue = defineModel<boolean>();
</script>

<template>
    <div class="uu-form-field">
        <div class="form-check">
            <input
                :id="question.id"
                v-model="modelValue"
                type="checkbox"
                class="form-check-input"
            />
            <label :for="question.id" class="form-check-label">{{
                useTranslateableAttribute(question, "text")
            }}</label>
        </div>
        <p
            v-if="question.descriptionNl || question.descriptionEn"
            class="text-muted"
        >
            {{ useTranslateableAttribute(question, "description") }}
        </p>
    </div>
</template>
