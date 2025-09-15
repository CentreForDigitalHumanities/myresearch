<script setup lang="ts">
import scale from "assets/images/icons/scale.png";
import pencil from "assets/images/icons/pencil.png";
let status = "DRAFT";

const refNumber = "234324_2025";
const title = "Voorstel Kattenbiologie";
const type = "proposal_in_ethics";
let statusIcon = "";
let buttonText = "";
let dateSubmitted = "2025-01-24";
let lastEdited = "2025-04-23";
if (status === "DRAFT") {
  statusIcon = pencil;
  buttonText = "Continue";
} else if (status === "SUBMITTED_TO_SUPERVISOR") {
  statusIcon = scale;
  buttonText = "Assess";
}
type roadmap = {
  refNumber: number;
};
type status = "DRAFT" | "SUBMITTED_TO_SUPERVISOR";
type proposal = {
  refNumber: number;
  title: string;
  type: string;
  status: status;
  dateSubmitted: string;
  lastEdited: string;
};
type editable = proposal; // | roadmap | etc.

const lastProposal: proposal = {
  refNumber: 234324_2025,
  title: "Voorstel Kattenbiologie",
  type: "proposal_in_ethics",
  status: "DRAFT",
  dateSubmitted: "2025-01-24",
  lastEdited: "2025-04-23",
};
const editables: editable[] = [
  lastProposal,
  {
    refNumber: 4,
    title: "hi",
    type: "proposal_in_ethics",
    status: "SUBMITTED_TO_SUPERVISOR",
    dateSubmitted: "2025-01-24",
    lastEdited: "2025-04-23",
  },
];
</script>

<template>
  <h2 class="uu-sidebar-header-linked">{{ $t("Recent Activity") }}</h2>
  <div v-for="editable in editables" class="card mb-2 text-bg-light mw-100">
    <div class="card-body mw-100">
      <div class="d-flex align-items-center mw-100">
        <h3 class="card-title">{{ editable.refNumber }}</h3>
        <div class="text-muted ms-auto">
          {{ $t("Last edited") }}: {{ editable.lastEdited }}
        </div>
      </div>
      <h5 class="card-title">{{ editable.title }}</h5>
      <div class="text-muted mw-100">
        <div class="mw-100">{{ $t("Type") }}: {{ editable.type }}</div>
        <div class="mw-100">
          {{ $t("Status") }}:
          <img
            v-if="editable.status == 'DRAFT'"
            :src="pencil"
            alt="pencil.png"
          />
          <img
            v-else-if="editable.status == 'SUBMITTED_TO_SUPERVISOR'"
            :src="scale"
            alt="scale.png"
          />
          {{ editable.status }}
        </div>
        <div class="mw-100">
          <p>{{ $t("Date submitted") }}: {{ editable.dateSubmitted }}</p>
        </div>
      </div>
      <div class="d-flex mt-3 mw-100">
        <NuxtLink href="#" class="ms-auto btn btn-primary btn-arrow-right">
          <span v-if="editable.status == 'DRAFT'">{{ $t("Continue") }}</span>
          <span v-if="editable.status == 'SUBMITTED_TO_SUPERVISOR'">{{
            $t("Assess")
          }}</span>
        </NuxtLink>
      </div>
    </div>
  </div>
</template>
