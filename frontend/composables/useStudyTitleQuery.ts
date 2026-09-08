import { computed, type Ref } from "vue";
import { useQuery } from "@vue/apollo-composable";
import { graphql } from "~/generated/gql";
import type { GetStudyTitleQuery } from "~/generated/gql/graphql";

const GET_STUDY_TITLE = graphql(`
    query GetStudyTitle($id: ID!) {
        study(id: $id, mrPermission: "View") {
            id
            title
            reference
        }
    }
`);

export function useStudyTitleQuery(studyId: Ref<string | undefined>) {
    const { result: studyResult } = useQuery<GetStudyTitleQuery>(
        GET_STUDY_TITLE,
        () => ({ id: studyId.value }),
        () => ({ enabled: !!studyId.value }),
    );

    return computed(() => studyResult.value?.study ?? null);
}
