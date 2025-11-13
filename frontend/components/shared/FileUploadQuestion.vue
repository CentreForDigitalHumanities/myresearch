<script lang="ts" setup>
import type { FileUploadQuestionType } from "~/generated/gql/graphql";

interface Props {
    question: Pick<
        FileUploadQuestionType,
        | "id"
        | "textNl"
        | "textEn"
        | "descriptionNl"
        | "descriptionEn"
        // Not currently enforced.
        | "sizeLimit"
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
        <input :id="question.id" type="file" class="form-control" />
    </div>
</template>
