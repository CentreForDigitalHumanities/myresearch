<script lang="ts" setup>
import { useQuery } from "@vue/apollo-composable";
import { graphql } from "~/generated/gql";
import type { GetFormQuery } from "~/generated/gql/graphql";
import FormWrapper from "~/components/shared/FormWrapper.vue";

const GET_FORM = graphql(`
    query GetForm {
        form {
            id
            nameEn
            nameNl
            steps {
                id
                slug
                nameEn
                nameNl
                descriptionEn
                descriptionNl
                ...FormInfoFragment
                questions {
                    id
                    textEn
                    textNl
                    descriptionEn
                    descriptionNl
                    required
                    ... on SelectQuestionType {
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
                }
                substeps {
                    id
                    slug
                    nameEn
                    nameNl
                    descriptionEn
                    descriptionNl
                    ...FormInfoFragment
                    questions {
                        id
                        textEn
                        textNl
                        descriptionEn
                        descriptionNl
                        required
                        ... on SelectQuestionType {
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
                    }
                }
            }
        }
    }
`);

const { result: formResult } = useQuery<GetFormQuery>(GET_FORM);

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
                :form="form"
                :current-step-slug="stepSlug(route.params.slug)"
            />
        </div>
    </div>
</template>
