<script lang="ts" setup>
import type { SelectQuestionWithValue } from "~/composables/useProcessForm";
import FormLabel from "../form/FormLabel.vue";
import { BSMultiSelect } from "cdh-vue-lib";

interface Props {
    question: SelectQuestionWithValue;
    isInvalid: boolean;
}

const props = defineProps<Props>();

// The parent treats the value as a string.
const modelValue = defineModel<string>();

// For multiselect, convert between comma-separated string and array
const multiSelectValue = computed({
    get: () => {
        if (!modelValue.value || modelValue.value.trim() === "") {
            return [];
        }
        // Parse comma-separated string to array
        return modelValue.value
            .split(",")
            .map((v) => v.trim())
            .filter((v) => v);
    },
    set: (newValue: string[]) => {
        modelValue.value = newValue.join(",");
    },
});

const options = computed<[string, string][]>(() => {
    return props.question.options.map((option) => [
        option.id,
        useTranslateableAttribute(option, "label"),
    ]);
});
</script>

<template>
    <div>
        <FormLabel :question="question" />
        <div
            v-if="question.descriptionNl || question.descriptionEn"
            class="text-muted"
            v-html="useTranslateableAttribute(question, 'description')"
        ></div>
        <BSMultiSelect
            v-if="question.multiple"
            v-model="multiSelectValue"
            :options="options"
        />
        <select
            v-else
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
