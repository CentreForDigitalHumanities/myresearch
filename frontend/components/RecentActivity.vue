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
</script>

<template>
  <h2 class="uu-sidebar-header-linked">{{ $t("Recent Activity") }}</h2>
  <div class="card mb-2 text-bg-light mw-100">
    <div class="card-body mw-100">
      <div class="d-flex align-items-center mw-100">
        <h3 class="card-title">{{ refNumber }}</h3>
        <div class="text-muted ms-auto">
          {{ $t("Last edited") }}: {{ lastEdited }}
        </div>
      </div>
      <h5 class="card-title">{{ title }}</h5>
      <div class="text-muted mw-100">
        <div class="mw-100">{{ $t("Type") }}: {{ type }}</div>
        <div class="mw-100">
          {{ $t("State") }}: <img :src="statusIcon" class="" alt="card_img" />
          {{ status }}
        </div>
        <div class="mw-100">
          <p>{{ $t("Date submitted") }}: {{ dateSubmitted }}</p>
        </div>
      </div>
      <div class="d-flex mt-3 mw-100">
        <NuxtLink href="#" class="ms-auto btn btn-primary btn-arrow-right">
          {{ $t(buttonText) }}
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.tiles .tile {
  aspect-ratio: 2/1;

  &:hover {
    background: white;
  }
}
</style>
