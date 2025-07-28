<script lang="ts" setup>
import { mockVwr } from "~/components/proc-reg/mockConfig";

const formConfig = mockVwr;
</script>

<template>
  <div class="uu-content">
    <Title>{{ $t("Processing Registry") }}</Title>
    <div class="uu-hero">
      <h1>{{ $t("Processing Registry") }}</h1>
    </div>
    <div class="uu-container">
      <SharedMRForm :form-config="formConfig" />
    </div>
  </div>
</template>
