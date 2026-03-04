<script lang="ts" setup>
import type { SelectQuestionWithValue } from "~/composables/useProcessForm";
import FormLabel from "./FormLabel.vue";

interface Props {
    question: SelectQuestionWithValue;
    isInvalid: boolean;
}

defineProps<Props>();

const modelValue = defineModel<string>();
</script>

<template>
    <div>
        <FormLabel :question="question" />
        <p
            v-if="question.descriptionNl || question.descriptionEn"
            class="text-muted"
        >
            {{ useTranslateableAttribute(question, "description") }}
        </p>
        <select
            :id="`${question.questionId}-${question.repeatIndex}`"
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
