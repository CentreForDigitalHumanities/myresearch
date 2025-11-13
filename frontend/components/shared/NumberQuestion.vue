<script lang="ts" setup>
import type { NumberQuestionType } from "~/generated/gql/graphql";

interface Props {
    question: Pick<
        NumberQuestionType,
        | "id"
        | "textNl"
        | "textEn"
        | "descriptionNl"
        | "descriptionEn"
        | "positiveOnly"
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
            :id="question.id"
            type="number"
            class="form-control"
            :min="question.positiveOnly ? 0 : undefined"
        />
    </div>
</template>
