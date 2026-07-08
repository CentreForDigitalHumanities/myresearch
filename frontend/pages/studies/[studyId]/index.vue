<script lang="ts" setup>
import { useQuery } from "@vue/apollo-composable";
import { graphql } from "~/generated/gql";
import type { GetStudyQuery } from "~/generated/gql/graphql";
import StudyDetailsSidebar from "~/components/studyDetail/StudyDetailsSidebar.vue";
import AvailableActions from "~/components/studyDetail/AvailableActions.vue";
import StudyProgressBar from "~/components/studyDetail/StudyProgressBar.vue";
import { useStudyId } from "~/composables/useRouteParams";

const currentUserStore = useCurrentUserStore();
await callOnce("user", () => currentUserStore.loadData());

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

// If study is even, it is a draft. If it is odd, it is in the review phase
const studyStatus = computed(() =>
    Number(study.value?.id) % 2 === 0 ? "draft" : "review",
);
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
                            <span
                                v-if="
                                    currentUserStore.currentUser
                                        ?.isPrivacyOfficer && study.isSeen
                                "
                                class="badge rounded-pill text-bg-info mb-1 fs-6"
                                >Seen</span
                            >
                            <h1>
                                {{ study.reference }} -
                                <em>{{ study.title }}</em>
                            </h1>
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
                            <StudyProgressBar :study-status="studyStatus" />
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
