<script lang="ts" setup>
import type { TextQuestion } from "../form/types";

interface Props {
    question: TextQuestion;
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
        <input
            v-if="!question.lines || question.lines < 2"
            :id="question.id"
            type="text"
            class="form-control"
        />
        <textarea
            v-if="question.lines && question.lines >= 2"
            :id="question.id"
            class="form-control"
            :rows="question.lines"
        ></textarea>
    </div>
</template>
