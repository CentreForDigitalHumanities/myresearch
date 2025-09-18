<script lang="ts" setup>
import type { TrueFalseQuestionType } from "~/generated/gql/graphql";

interface Props {
    question: Pick<
        TrueFalseQuestionType,
        | "id"
        | "textNl"
        | "textEn"
        | "descriptionNl"
        | "descriptionEn"
        | "defaultValue"
    >;
}

defineProps<Props>();
</script>

<template>
    <div class="uu-form-field">
        <div class="form-check">
            <input
                :id="question.id"
                type="checkbox"
                class="form-check-input"
                :checked="question.defaultValue"
            />
            <label :for="question.id" class="form-check-label">{{
                useTranslateableAttribute(question, "text")
            }}</label>
        </div>
        <p
            v-if="question.descriptionNl || question.descriptionEn"
            class="text-muted"
        >
            {{ useTranslateableAttribute(question, "description") }}
        </p>
    </div>
</template>
