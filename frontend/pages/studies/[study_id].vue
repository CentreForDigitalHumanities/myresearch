<script lang="ts" setup>
import { useQuery } from "@vue/apollo-composable";
import { graphql } from "~/generated/gql";
import type { GetStudyQuery } from "~/generated/gql/graphql";
import { showError, createError } from "#app";

// retrieve study

const GET_STUDY = graphql(`
    query GetStudy($id: ID!) {
        study(id: $id, mrPermission: "View") {
            createdBy {
                fullName
                id
                email
            }
            id
            title
        }
    }
`);

const route = useRoute();

const {
    result: studyResult,
    loading,
    error,
} = useQuery<GetStudyQuery>(GET_STUDY, { id: route.params.study_id });

const study = computed(() => studyResult.value?.study ?? null);

// Give 404 if the study does not exist

watchEffect(() => {
    if (!loading.value && studyResult.value && !study.value) {
        showError(
            createError({ statusCode: 404, statusMessage: "Study not found" }),
        );
    }
});

// Some functions to generate mockdates

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

    // Format as DD-MM-YYYY
    const dd = String(randomDate.getDate()).padStart(2, "0");
    const mm = String(randomDate.getMonth() + 1).padStart(2, "0"); // months are 0-based
    const yyyy = randomDate.getFullYear();

    return `${dd}-${mm}-${yyyy}`;
}

function randomNumber100to1000(): number {
    return Math.floor(Math.random() * (1000 - 100 + 1)) + 100;
}
</script>

<template>
    <div class="uu-content">
        <Title>{{ $t("Study") }}: {{ study?.title }}</Title>
        <div class="uu-hero">
            <h1>{{ $t("Study overview") }}: {{ study?.title }}</h1>
        </div>
        <!-- Sidebar -->
        <div class="uu-sidebar-container">
            <aside class="uu-sidebar">
                <button
                    class="uu-sidebar-toggle"
                    type="button"
                    data-bs-toggle="collapse"
                    data-bs-target="#exampleSidebar"
                    aria-expanded="false"
                >
                    {{ $t("Show sidebar") }}
                </button>
                <div id="exampleSidebar" class="uu-sidebar-collapse collapse">
                    <h3>{{ $t("Creator details") }}</h3>
                    <ul>
                        <li class="mt-2">
                            {{ $t("Created by:") }}
                            {{ study?.createdBy.fullName }}
                        </li>
                        <li class="mt-2">
                            {{ $t("Creator email:") }}
                            {{ study?.createdBy.email }}
                        </li>
                    </ul>
                    <h3>{{ $t("Study details:") }}</h3>
                    <ul>
                        <li class="mt-2">
                            {{ $t("Created on:") }} {{ randomDatePastYear() }}
                        </li>
                        <li class="mt-2">
                            {{ $t("Submitted on:") }} {{ randomDatePastYear() }}
                        </li>
                    </ul>
                </div>
            </aside>
            <!-- Content -->
            <div class="uu-sidebar-content">
                <div class="uu-container">
                    <div class="row">
                        <!-- Main Content -->
                        <div class="col me-5">
                            <h1>
                                2025-{{ randomNumber100to1000() }} -
                                {{ study?.title }} {{ $t("Overview") }}
                            </h1>
                            <p>
                                {{
                                    $t(
                                        "This page shows and overview of the status and available actions for the study",
                                    )
                                }}
                                <em>{{ study?.title }}</em
                                >.
                            </p>
                            <h3>Available actions:</h3>
                            <div class="tiles">
                                <a class="tile h-100">
                                    <strong>{{ $t("View PDF") }}</strong>
                                </a>
                                <a class="tile h-100">
                                    <strong>{{
                                        $t("View attachments")
                                    }}</strong>
                                </a>
                                <a class="tile h-100">
                                    <strong>{{ $t("Submit decision") }}</strong>
                                </a>
                            </div>
                        </div>
                        <!-- Progess bar -->
                        <div class="col-2">
                            <div class="stepper h-100">
                                <ul
                                    class="h-100 d-flex flex-column justify-content-between"
                                >
                                    <li>
                                        <a class="stepper-item">
                                            <span
                                                class="stepper-bubble stepper-bubble-largest complete"
                                            ></span>
                                            <span>{{ $t("Created") }}</span>
                                        </a>
                                    </li>
                                    <li>
                                        <a class="stepper-item">
                                            <span
                                                class="stepper-bubble stepper-bubble-largest complete"
                                            ></span>
                                            <span>{{
                                                $t("Submitted for review")
                                            }}</span>
                                        </a>
                                    </li>
                                    <li>
                                        <a class="stepper-item active">
                                            <span
                                                class="stepper-bubble stepper-bubble-largest incomplete"
                                            ></span>
                                            <span class="text-wrap">{{
                                                $t(
                                                    "Review from Privacy Officer",
                                                )
                                            }}</span>
                                        </a>
                                    </li>
                                    <li>
                                        <a class="stepper-item">
                                            <span
                                                class="stepper-bubble stepper-bubble-largest"
                                            ></span>
                                            <span class="text-wrap">{{
                                                $t("Conclusion")
                                            }}</span>
                                        </a>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
