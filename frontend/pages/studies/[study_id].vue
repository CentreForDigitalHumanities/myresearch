<script lang="ts" setup>
import { useQuery } from "@vue/apollo-composable";
import { graphql } from "~/generated/gql";
import type { GetStudyQuery } from "~/generated/gql/graphql";
import { showError, createError } from "#app";
import StudyDetailsSidebar from "../../components/study_detail/StudyDetailsSidebar.vue";
import AvailableActions from "../../components/study_detail/AvailableActions.vue";
import StudyProgessBar from "../../components/study_detail/StudyProgessBar.vue";

const GET_STUDY = graphql(`
    query GetStudy($id: ID!) {
        study(id: $id, mrPermission: "View") {
            id
            title
            reference
            latestSubmissionId
            createdBy {
                fullName
                id
                email
            }
        }
    }
`);

const route = useRoute();

const { result: studyResult } = useQuery<GetStudyQuery>(GET_STUDY, {
    id: route.params.study_id,
});

const study = computed(() => studyResult.value?.study ?? null);

// Some functions to generate mockdata

function randomDatePastYear(): string {
    const today = new Date();
    const oneYearAgo = new Date();
    oneYearAgo.setFullYear(today.getFullYear() - 1);

    // Get timestamps
    const start = oneYearAgo.getTime();
    const end = today.getTime();

    // Pick a random timestamp between start and end
    const randomTime = start + Math.random() * (end - start);
    const randomDate = new Date(randomTime);

    return randomDate.toISOString().split("T")[0];
}

// If study is even, it is a draft. If it is odd, it is in the review phase

const studyStatus = computed(() =>
    Number(study.value?.id) % 2 === 0 ? "draft" : "review",
);
</script>

<template>
    <div class="uu-content">
        <Title
            >{{ $t("Study") }}: {{ study?.title ?? $t("Unknown study") }}</Title
        >
        <div class="uu-hero">
            <h1>{{ $t("Study overview") }}</h1>
        </div>
        <!-- Sidebar -->
        <div v-if="study" class="uu-sidebar-container">
            <StudyDetailsSidebar
                :study="study"
                :random-date-past-year="randomDatePastYear()"
            />
            <!-- Content -->
            <div class="uu-sidebar-content">
                <div class="uu-container">
                    <div class="row">
                        <!-- Main Content -->
                        <div class="col me-5">
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
                                :study-status="studyStatus"
                                :submission-id="study.latestSubmissionId"
                            />
                        </div>
                        <!-- Progess bar -->
                        <div class="col-2">
                            <StudyProgessBar :study-status="studyStatus" />
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="uu-container" v-else>
            <h3>
                {{
                    $t(
                        "Oops ... The study you are looking for could not be found.",
                    )
                }}
            </h3>
        </div>
    </div>
</template>
