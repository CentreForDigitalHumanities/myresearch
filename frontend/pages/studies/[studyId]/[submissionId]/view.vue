<script lang="ts" setup>
import { BSButton } from "cdh-vue-lib";
import OverviewWrapper from "~/components/form/overview/OverviewWrapper.vue";
import { useSubmissionId, useStudyId } from "~/composables/useRouteParams";
import { useFormQuery } from "~/composables/useFormQuery";
import { useStudyTitleQuery } from "~/composables/useStudyTitleQuery";
import Loading from "~/components/shared/Loading.vue";

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
        <div
            class="uu-hero d-flex flex-nowrap justify-content-between align-items-center gap-3"
        >
            <BSButton
                variant="secondary"
                class="btn-arrow-left flex-shrink-0"
                @click="goBackToStudy"
            >
                {{ $t("Go back to study page") }}
            </BSButton>
            <h1 class="mb-0 text-wrap text-break">
                {{ study?.reference }} -
                {{ study?.title }}
            </h1>
        </div>
        <div class="uu-container">
            <div class="col-12">
                <OverviewWrapper v-if="form" :queried-form="form" />
                <div v-else>
                    <Loading />
                    <br class="mb-4" />
                </div>
                <BSButton
                    variant="primary"
                    class="btn-arrow-left"
                    @click="goBackToStudy"
                >
                    {{ $t("Go back to study page") }}
                </BSButton>
            </div>
        </div>
    </div>
</template>
