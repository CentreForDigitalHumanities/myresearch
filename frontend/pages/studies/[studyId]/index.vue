<script lang="ts" setup>
import { useQuery } from "@vue/apollo-composable";
import { graphql } from "~/generated/gql";
import type { GetStudyQuery } from "~/generated/gql/graphql";
import StudyDetailsSidebar from "~/components/studyDetail/StudyDetailsSidebar.vue";
import AvailableActions from "~/components/studyDetail/AvailableActions.vue";
import StudyProgressBar from "~/components/studyDetail/StudyProgressBar.vue";
import { SubmissionStatus } from "~/generated/gql/graphql";
import { useStudyId } from "~/composables/useRouteParams";

const currentUserStore = useCurrentUserStore();
await callOnce("user", () => currentUserStore.loadData());

const currentUser = computed(() => useCurrentUserStore().currentUser);

const GET_STUDY = graphql(`
    query GetStudy($id: ID!) {
        study(id: $id, mrPermission: "View") {
            id
            title
            reference
            latestSubmissionId
            actions
            createdAt
            updatedAt
            isSeen
            createdBy {
                fullName
                id
                email
            }
            statuses {
                id
                status
                createdAt
            }
        }
    }
`);

const studyId = useStudyId();

const { result: studyResult } = useQuery<GetStudyQuery>(
    GET_STUDY,
    () => ({ id: studyId.value }),
    () => ({ enabled: !!studyId.value }),
);

const study = computed(() => studyResult.value?.study ?? null);
const statuses = computed(() => study.value?.statuses ?? []);

const isSubmitted = computed(() => {
    const lastStatus = statuses.value.at(-1)?.status;
    return lastStatus === SubmissionStatus.Submitted;
});
</script>

<template>
    <div class="uu-content">
        <Title>
            {{ $t("Study") }}: {{ study?.title ?? $t("Unknown study") }}
        </Title>
        <div class="uu-hero">
            <h1>{{ $t("Study overview") }}</h1>
        </div>
        <div v-if="study" class="uu-sidebar-container">
            <StudyDetailsSidebar :study="study" />
            <div class="uu-sidebar-content">
                <div class="uu-container">
                    <div class="row">
                        <div class="col me-5">
                            <div v-if="study.isSeen !== null">
                                <span
                                    v-if="study.isSeen"
                                    class="badge rounded-pill text-bg-info mb-1 fs-6"
                                    >{{ $t("Seen") }}</span
                                >
                                <span
                                    v-else
                                    class="badge rounded-pill text-bg-gray mb-1 fs-6"
                                    >{{ $t("Unseen") }}</span
                                >
                            </div>
                            <h1>
                                {{ study.reference }} -
                                <em>{{ study.title }}</em>
                            </h1>
                            <div
                                v-if="
                                    isSubmitted &&
                                    currentUser?.id === study.createdBy.id
                                "
                                class="alert alert-info"
                            >
                                {{
                                    $t(
                                        "Your study has been submitted. If you'd like to make any further changes, please contact the Privacy Officer:",
                                    )
                                }}
                                <a href="mailto:privacy.gw@uu.nl"
                                    >privacy.gw@uu.nl</a
                                >
                                /
                                <a href="mailto:privacy.rebo@uu.nl"
                                    >privacy.rebo@uu.nl</a
                                >
                            </div>
                            <p>
                                {{
                                    $t(
                                        "This page shows and overview of the status and available actions for the study",
                                    )
                                }}
                                <em>{{ study.title }}</em
                                >.
                            </p>
                            <AvailableActions
                                :study-id="study.id"
                                :submission-id="study.latestSubmissionId"
                            />
                        </div>
                        <div class="col-2">
                            <StudyProgressBar
                                v-if="statuses.length > 0"
                                :statuses="statuses"
                            />
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div v-else class="uu-container">
            <h3>
                {{ $t("The study you are looking for could not be found.") }}
            </h3>
        </div>
    </div>
</template>
