<script lang="ts" setup>
import type { SelectQuestion } from "../form/types";

interface Props {
    question: SelectQuestion;
}

defineProps<Props>();
</script>

<template>
    <div class="uu-form-field">
        <label :for="question.id" class="form-label">{{
            useTranslateableAttribute(question, "label")
        }}</label>
        <p
            v-if="question.descriptionNl || question.descriptionEn"
            class="text-muted"
        >
            {{ useTranslateableAttribute(question, "description") }}
        </p>
        <select :id="question.id" class="form-control">
            <option
                v-for="option in question.options"
                :key="option.value"
                :value="option.value"
            >
                {{ useTranslateableAttribute(option, "label") }}
            </option>
        </select>
    </div>
</template>
