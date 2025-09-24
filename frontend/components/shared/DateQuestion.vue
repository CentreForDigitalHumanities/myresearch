<script lang="ts" setup>
import type { DateQuestionType } from "~/generated/gql/graphql";

interface Props {
    question: Pick<
        DateQuestionType,
        "id" | "textNl" | "textEn" | "descriptionNl" | "descriptionEn"
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
        <input :id="question.id" type="date" class="form-control" />
    </div>
</template>
