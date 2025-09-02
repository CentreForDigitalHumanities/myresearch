<script lang="ts" setup>
import { mockVwr } from "~/components/form/procRegMockConfig";

const formConfig = mockVwr;

function stepSlug(route: string | string[]): string {
    return Array.isArray(route) ? route[0] : route;
}

const route = useRoute();
</script>

<template>
    <div class="uu-content">
        <Title>{{ $t("Processing Registry") }}</Title>
        <div class="uu-hero">
            <h1>{{ $t("Processing Registry") }}</h1>
        </div>
        <div class="uu-container">
            <SharedMRForm
                :form-config="formConfig"
                :current-step-slug="stepSlug(route.params.step)"
            />
        </div>
    </div>
</template>
