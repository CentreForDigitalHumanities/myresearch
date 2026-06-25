<script setup lang="ts">
import { Scale, Pencil } from "lucide-vue-next";

type Status = "DRAFT" | "SUBMITTED_TO_SUPERVISOR";
type Proposal = {
    refNumber: number; // refNumber doesn't show the _, waiting for backend to decide what it should be.
    title: string;
    type: string;
    status: Status;
    dateSubmitted: string;
    lastEdited: string;
};
type Intake = {
    refNumber: number;
    intakeBody: string;
    stepsCompleted: string;
};

const recentActivity: RecentActivity[] = [];
type RecentActivity = Proposal | Intake;

const isProposal = (
    recentActivity: RecentActivity,
): recentActivity is Proposal => {
    return recentActivity.hasOwnProperty("status");
};

const isIntake = (recentActivity: RecentActivity): recentActivity is Intake => {
    return recentActivity.hasOwnProperty("intakeBody");
};
</script>

<template>
    <h2 v-if="recentActivity.length !== 0" class="uu-sidebar-header-linked">
        {{ $t("Recent Activity") }}
    </h2>
    <div
        v-for="activity in recentActivity"
        class="card mb-2 text-bg-light mw-100"
    >
        <div class="card-body mw-100">
            <template v-if="isProposal(activity)">
                <div class="d-flex align-items-center mw-100">
                    <h3 class="card-title">{{ activity.refNumber }}</h3>
                    <div class="text-muted ms-auto">
                        {{ $t("Last edited") }}: {{ activity.lastEdited }}
                    </div>
                </div>
                <h5 class="card-title">{{ activity.title }}</h5>
                <div class="text-muted mw-100">
                    <div class="mw-100">
                        {{ $t("Type") }}: {{ activity.type }}
                    </div>
                    <div class="mw-100">
                        {{ $t("Status") }}:
                        <template v-if="activity.status == 'DRAFT'">
                            <Pencil class="icon" />
                        </template>
                        <template
                            v-if="activity.status == 'SUBMITTED_TO_SUPERVISOR'"
                            ><Scale class="icon"
                        /></template>
                        {{ activity.status }}
                    </div>
                    <div class="mw-100">
                        <p>
                            {{ $t("Date submitted") }}:
                            {{ activity.dateSubmitted }}
                        </p>
                    </div>
                </div>
                <div class="d-flex mt-3 mw-100">
                    <NuxtLink
                        href="#"
                        class="ms-auto btn btn-primary btn-arrow-right"
                    >
                        <span v-if="activity.status == 'DRAFT'">{{
                            $t("Continue")
                        }}</span>
                        <span
                            v-if="activity.status == 'SUBMITTED_TO_SUPERVISOR'"
                            >{{ $t("Assess") }}</span
                        >
                    </NuxtLink>
                </div>
            </template>
            <template v-if="isIntake(activity)">
                <h3 class="card-title">{{ activity.refNumber }}</h3>
                <div>{{ activity.intakeBody }}</div>
                <div>
                    {{ $t("Steps completed") }}: {{ activity.stepsCompleted }}
                </div>
                <div class="d-flex mt-3 mw-100">
                    <NuxtLink
                        href="#"
                        class="ms-auto btn btn-primary btn-arrow-right"
                        >{{ $t("View Conclusion") }}
                    </NuxtLink>
                </div>
            </template>
        </div>
    </div>
</template>
<style lang="scss" scoped>
.icon {
    color: black;
    height: 1em;
    width: 1em;
    margin-bottom: 5px;
}
</style>
