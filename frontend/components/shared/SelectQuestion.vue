<script lang="ts" setup>
import type { SelectQuestionType } from "~/generated/gql/graphql";

interface Props {
    question: Pick<
        SelectQuestionType,
        | "id"
        | "textNl"
        | "textEn"
        | "descriptionNl"
        | "descriptionEn"
        | "options"
        | "multiple"
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
        <select :id="question.id" class="form-control">
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
