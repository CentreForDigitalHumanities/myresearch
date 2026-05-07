<script lang="ts" setup>
import { useQuery } from "@vue/apollo-composable";
import { graphql } from "~/generated/gql";
import type { GetFormQuery } from "~/generated/gql/graphql";
import FormWrapper from "~/components/form/FormWrapper.vue";

const GET_FORM = graphql(`
  query GetForm($submissionId: ID!) {
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

const route = useRoute();

const submissionId = computed(() => {
  const id = route.params.submissionId;
  return Array.isArray(id) ? id[0] : id;
});

const { result: formResult } = useQuery<GetFormQuery>(
  GET_FORM,
  () => ({
    submissionId: submissionId.value,
  }),
  () => ({
    enabled: !!submissionId.value,
  }),
);

const form = computed(() => formResult.value?.form ?? null);

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
      />
    </div>
  </div>
</template>
