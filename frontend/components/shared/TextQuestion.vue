<script lang="ts" setup>
import type { TextQuestionType } from "~/generated/gql/graphql";

interface Props {
    question: Pick<
        TextQuestionType,
        | "id"
        | "textNl"
        | "textEn"
        | "descriptionNl"
        | "descriptionEn"
        | "placeholderNl"
        | "placeholderEn"
        | "lines"
    >;
}

defineProps<Props>();
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
