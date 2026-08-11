<script lang="ts" setup>
import OverviewWrapper from "~/components/form/overview/OverviewWrapper.vue";
import { useSubmissionId, useStudyId } from "~/composables/useRouteParams";
import { useFormQuery } from "~/composables/useFormQuery";
import { useStudyTitleQuery } from "~/composables/useStudyTitleQuery";
import Loading from "~/components/shared/Loading.vue";
import { MoveLeft } from "lucide-vue-next";

const submissionId = useSubmissionId();
const form = useFormQuery(submissionId, "View");

const studyId = useStudyId();
const study = useStudyTitleQuery(studyId);

function goBackToStudy() {
    return navigateTo({
        name: "studies-studyId",
        params: { studyId: studyId.value },
    });
}
</script>

<template>
    <div class="uu-content">
        <Title>{{ study?.reference }} - {{ study?.title }}</Title>
        <div class="uu-hero">
            <h1 class="text-wrap text-break">
                {{ study?.reference }} -
                {{ study?.title }}
            </h1>
        </div>
        <div class="uu-container">
            <div class="mb-3">
                <a href="#" class="pe-auto" @click.prevent="goBackToStudy">
                    <div class="d-flex gap-2 align-items-center">
                        <MoveLeft class="icon" />
                        <div class="ml-3">
                            {{ $t("Go back to study page") }}
                        </div>
                    </div>
                </a>
            </div>
            <div class="col-12">
                <OverviewWrapper v-if="form" :queried-form="form" />
                <div v-else>
                    <Loading />
                    <br class="mb-4" />
                </div>
                <div class="mb-3">
                    <a href="#" class="pe-auto" @click.prevent="goBackToStudy">
                        <div class="d-flex gap-2 align-items-center">
                            <MoveLeft class="icon" />
                            <div class="ml-3">
                                {{ $t("Go back to study page") }}
                            </div>
                        </div>
                    </a>
                </div>
            </div>
        </div>
    </div>
</template>
