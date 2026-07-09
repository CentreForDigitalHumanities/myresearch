<script lang="ts" setup>
import { useQuery } from "@vue/apollo-composable";
import { graphql } from "~/generated/gql";
import { BSButton } from "cdh-vue-lib";
import type {
    GetFormOverviewQuery,
    GetStudyTitleQuery,
} from "~/generated/gql/graphql";
import OverviewWrapper from "~/components/form/overview/OverviewWrapper.vue";
import { useSubmissionId, useStudyId } from "~/composables/useRouteParams";
import Loading from "~/components/shared/Loading.vue";

const GET_FORM = graphql(`
    query GetFormOverview($submissionId: ID!) {
        form(submissionId: $submissionId, mrPermission: "View") {
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

const form = computed(() => formResult.value?.form ?? null);

const GET_STUDY = graphql(`
    query GetStudyTitle($id: ID!) {
        study(id: $id, mrPermission: "View") {
            id
            title
            reference
        }
    }
`);

const studyId = useStudyId();

const { result: studyResult } = useQuery<GetStudyTitleQuery>(
    GET_STUDY,
    () => ({ id: studyId.value }),
    () => ({ enabled: !!studyId.value }),
);

const study = computed(() => studyResult.value?.study ?? null);
</script>

<template>
    <div class="uu-content">
        <Title>{{ $t("Registration overview") }}</Title>
        <div class="uu-hero">
            <h1>{{ $t("Registration overview") }}</h1>
        </div>
        <div class="uu-container">
            <div class="col-12">
                <h1>
                    {{ study?.reference }} - <em>{{ study?.title }}</em>
                </h1>
                <hr />
                <OverviewWrapper v-if="form" :queried-form="form" />
                <div v-else>
                    <Loading />
                    <br class="mb-4" />
                </div>
                <BSButton
                    variant="primary"
                    class="btn-arrow-left"
                    @click="
                        navigateTo({
                            name: 'studies-studyId',
                            params: { studyId },
                        })
                    "
                >
                    {{ $t("Go back to study page") }}
                </BSButton>
            </div>
        </div>
    </div>
</template>
