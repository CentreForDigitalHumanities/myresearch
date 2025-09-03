<script lang="ts" setup>
import { useQuery } from "@vue/apollo-composable";
import { graphql } from "~/generated/gql";
import type { GetFormQuery } from "~/generated/gql/graphql";

const GET_FORM = graphql(`
    query GetForm {
        form {
            id
            nameEn
            nameNl
            descriptionEn
            descriptionNl
            steps {
                id
                slug
                nameEn
                nameNl
                descriptionEn
                descriptionNl
                formOrder
                info {
                    ...StepInfoFragment
                }
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
                    parentOrder
                    info {
                        ...StepInfoFragment
                    }
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

function stepSlug(route: string | string[]): string {
    return Array.isArray(route) ? route[0] : route;
}

const route = useRoute();
</script>

<template>
    <div class="uu-content">
        <Title>{{ $t("Processing Registry") }}</Title>
        <div class="uu-hero">
            <h1>{{ $t("Processing Registry") }}</h1>
        </div>
        <div class="uu-container">
            <SharedMRForm
                v-if="form"
                :form="form"
                :current-step-slug="stepSlug(route.params.step)"
            />
        </div>
    </div>
</template>
