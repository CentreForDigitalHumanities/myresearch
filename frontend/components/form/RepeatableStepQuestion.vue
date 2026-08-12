<script lang="ts" setup>
import type { RepeatableStepQuestionWithValue } from "~/composables/useProcessForm";
import { useSubmissionId } from "~/composables/useRouteParams";
import FormLabel from "../form/FormLabel.vue";
import { BSButton } from "cdh-vue-lib";
import { useMutation } from "@vue/apollo-composable";
import { graphql } from "~/generated/gql";
import { useNotification } from "~/composables/useNotification";
import { useI18n } from "vue-i18n";
import { useTranslateableAttribute } from "~/composables/useLocalisation";

const submissionId = useSubmissionId();
const { t } = useI18n();

interface Props {
    question: RepeatableStepQuestionWithValue;
    isInvalid: boolean;
}

const props = defineProps<Props>();

const CREATE_STEP_REPEAT_MUTATION = graphql(`
    mutation CreateStepRepeat($userFormId: ID!, $repeatableId: ID!) {
        createRepeat(userFormId: $userFormId, repeatableId: $repeatableId) {
            newRepeatIndex
            errors {
                field
                messages
            }
        }
    }
`);

const { mutate: createStepRepeat } = useMutation(CREATE_STEP_REPEAT_MUTATION, {
    update: (cache) => {
        cache.evict({ fieldName: "form" });
        cache.gc();
    },
});

function handleAddStep(): void {
    const userFormId = submissionId.value;
    if (!userFormId) {
        return;
    }

    void createStepRepeat({
        userFormId,
        repeatableId: props.question.repeatableStepId,
    }).catch(() => {
        useNotification(
            t("An error occurred while adding a step. Please try again."),
            "danger",
        );
    });
}
</script>

<template>
    <FormLabel :question="question" />
    <div
        v-if="question.descriptionNl || question.descriptionEn"
        class="text-muted"
        v-html="useTranslateableAttribute(question, 'description')"
    ></div>
    <BSButton
        variant="light"
        class="w-100 align-self-stretch"
        @click="handleAddStep"
    >
        {{ $t("Click to add a step") }}
    </BSButton>
</template>
