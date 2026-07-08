<script lang="ts" setup>
import { useQuery } from "@vue/apollo-composable";
import { graphql } from "~/generated/gql";
import type { GetFormOverviewQuery } from "~/generated/gql/graphql";
import SubmissionOverview from "~/components/form/overview/OverviewForm.vue";
import { useSubmissionId } from "~/composables/useRouteParams";

const GET_FORM = graphql(`
    query GetFormOverview($submissionId: ID!) {
        form(submissionId: $submissionId, mrPermission: "Edit") {
            formId
            nameEn
            nameNl
            submissionId
            steps {
                stepId
                slug
                repeatIndex
                nameEn
                nameNl
                descriptionEn
                descriptionNl
                isOverview
                ...FormInfoFragment
                questions {
                    questionId
                    repeatIndex
                    answer
                    responseId
                    textEn
                    textNl
                    descriptionEn
                    descriptionNl
                    required
                    hasConditions
                    ... on SelectQuestionType {
                        multiple
                        options {
                            id
                            labelNl
                            labelEn
                            defaultSelected
                        }
                    }
                    ... on NumberQuestionType {
                        positiveOnly
                    }
                    ... on TrueFalseQuestionType {
                        defaultValue
                    }
                    ... on FileUploadQuestionType {
                        sizeLimit
                    }
                    ... on TextQuestionType {
                        placeholderNl
                        placeholderEn
                        lines
                        isEmail
                    }
                    ... on DateQuestionType {
                        futureOnly
                    }
                }
                substeps {
                    stepId
                    slug
                    repeatIndex
                    nameEn
                    nameNl
                    descriptionEn
                    descriptionNl
                    isOverview
                    ...FormInfoFragment
                    questions {
                        questionId
                        repeatIndex
                        answer
                        responseId
                        textEn
                        textNl
                        descriptionEn
                        descriptionNl
                        required
                        hasConditions
                        ... on SelectQuestionType {
                            multiple
                            options {
                                id
                                labelNl
                                labelEn
                                defaultSelected
                            }
                        }
                        ... on NumberQuestionType {
                            positiveOnly
                        }
                        ... on TrueFalseQuestionType {
                            defaultValue
                        }
                        ... on FileUploadQuestionType {
                            sizeLimit
                        }
                        ... on TextQuestionType {
                            placeholderNl
                            placeholderEn
                            lines
                            isEmail
                        }
                        ... on DateQuestionType {
                            futureOnly
                        }
                    }
                }
            }
        }
    }
`);

const submissionId = useSubmissionId();

const { result: formResult } = useQuery<GetFormOverviewQuery>(
    GET_FORM,
    () => ({ submissionId: submissionId.value }),
    () => ({ enabled: !!submissionId.value }),
);

const queried = computed(() => formResult.value?.form);
const { formObject } = useFormState(queried);
</script>

<template>
    <div class="uu-content">
        <Title>{{ $t("Registration overview") }}</Title>
        <div class="uu-hero">
            <h1>{{ $t("Registration overview") }}</h1>
        </div>
        <div class="uu-container">
            <div class="col-12">
                <SubmissionOverview v-if="formObject" :form="formObject" />
            </div>
        </div>
        >
    </div>
</template>
