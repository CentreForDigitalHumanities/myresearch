<script lang="ts" setup>
import type { RepeatableStepQuestionWithValue } from "~/composables/useProcessForm";
import FormLabel from "../form/FormLabel.vue";
import { BSButton } from "cdh-vue-lib";

interface Props {
    question: RepeatableStepQuestionWithValue;
    isInvalid: boolean;
}

defineProps<Props>();
</script>

<template>
    <FormLabel :question="question" />
    <div
        v-if="question.descriptionNl || question.descriptionEn"
        class="text-muted"
        v-html="useTranslateableAttribute(question, 'description')"
    ></div>
    <BSButton variant="light" class="w-100 align-self-stretch">
        {{ $t("Click to add a step") }}
    </BSButton>
</template>
