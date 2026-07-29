<script lang="ts" setup>
import { BSButton } from "cdh-vue-lib";
import OverviewWrapper from "~/components/form/overview/OverviewWrapper.vue";
import { useSubmissionId, useStudyId } from "~/composables/useRouteParams";
import { useFormQuery } from "~/composables/useFormQuery";
import { useStudyQuery } from "~/composables/useStudyQuery";
import Loading from "~/components/shared/Loading.vue";

const submissionId = useSubmissionId();
const form = useFormQuery(submissionId, "View");

const studyId = useStudyId();
const study = useStudyQuery(studyId);
</script>

<template>
    <div class="uu-content">
        <Title>{{ $t("Registration overview") }}</Title>
        <div class="uu-hero">
            <h1>{{ $t("Registration overview") }}</h1>
        </div>
        <div class="uu-container">
            <div class="col-12">
                <div class="row">
                    <div class="col-3 d-flex">
                        <BSButton
                            variant="primary"
                            class="btn-arrow-left align-self-center"
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
                    <div class="col-9 d-flex">
                        <h1 class="mb-0">
                            {{ study?.reference }} - <em>{{ study?.title }}</em>
                        </h1>
                    </div>
                </div>
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
