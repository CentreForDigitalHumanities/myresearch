<script lang="ts" setup>
import { useQuery } from "@vue/apollo-composable";
import { graphql } from "~/generated/gql";
import type { GetFormQuery } from "~/generated/gql/graphql";
import FormWrapper from "~/components/shared/FormWrapper.vue";

const GET_FORM = graphql(`
    query GetForm {
        form {
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

const { result: formResult, refetch } = useQuery<GetFormQuery>(GET_FORM);

const form = computed(() => formResult.value?.form ?? null);

const route = useRoute();

function stepSlug(route: string | string[]): string {
    return Array.isArray(route) ? route[0] : route;
}
</script>

<template>
    <div class="uu-content">
        <Title>{{ $t("Processing Registry") }}</Title>
        <div class="uu-hero">
            <h1>{{ $t("Processing Registry") }}</h1>
        </div>
        <div class="uu-container">
            <FormWrapper
                v-if="form"
                :queried-form="form"
                :current-step-slug="stepSlug(route.params.slug)"
                @form-saved="refetch()"
            />
        </div>
    </div>
</template>
