<script lang="ts" setup>
import type { SelectQuestionWithValue } from "~/composables/useProcessForm";

interface Props {
    question: SelectQuestionWithValue;
    isInvalid: boolean;
}

defineProps<Props>();

const modelValue = defineModel<string>();
</script>

<template>
    <div>
        <label :for="question.id" class="form-label">
            {{ useTranslateableAttribute(question, "text") }}
        </label>
        <p
            v-if="question.descriptionNl || question.descriptionEn"
            class="text-muted"
        >
            {{ useTranslateableAttribute(question, "description") }}
        </p>
        <select
            :id="question.id"
            v-model="modelValue"
            class="form-control"
            :class="{ 'is-invalid': isInvalid }"
        >
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
