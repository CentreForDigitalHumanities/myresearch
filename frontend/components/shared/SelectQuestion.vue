<script lang="ts" setup>
import type { SelectQuestionWithValue } from "~/composables/useBuildForm";

interface Props {
    question: SelectQuestionWithValue;
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
        <select :id="question.id" v-model="modelValue" class="form-control">
            <option disabled value="">
                {{ $t("Please select one") }}
            </option>
            <option
                v-for="option in question.options"
                :key="option.id"
                :selected="option.defaultSelected"
                :value="option.id"
            >
                {{ useTranslateableAttribute(option, "label") }}
            </option>
        </select>
    </div>
</template>
