import { useQuery } from "@vue/apollo-composable";
import { computed } from "vue";
import type { Ref, ComputedRef } from "vue";
import { graphql } from "~/generated/gql";
import type { GetFormQuery } from "~/generated/gql/graphql";

const GET_FORM = graphql(`
    query GetForm($submissionId: ID!, $mrPermission: String!) {
        form(submissionId: $submissionId, mrPermission: $mrPermission) {
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

export function useFormQuery(
    submissionId:
        | Ref<string | null | undefined>
        | ComputedRef<string | undefined>,
    mrPermission: "View" | "Edit",
) {
    const { result: formResult } = useQuery<GetFormQuery>(
        GET_FORM,
        () => ({ submissionId: submissionId.value, mrPermission }),
        () => ({ enabled: !!submissionId.value }),
    );

    return computed(() => formResult.value?.form ?? null);
}
