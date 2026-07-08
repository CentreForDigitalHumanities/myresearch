<script lang="ts" setup>
import type { FormWithValues } from "~/composables/useProcessForm";
import OverviewStep from "./OverviewStep.vue";
import { AlertTriangle } from "lucide-vue-next";

interface Props {
    form: FormWithValues;
}

const props = defineProps<Props>();

// Filter out the overview step itself.
const contentSteps = computed(() =>
    props.form.steps.filter((step) => !step.isOverview),
);
</script>

<template>
    <div v-for="step in contentSteps" :key="step.stepId" class="mb-4 p-2">
        <h3 class="d-flex align-items-center">
            {{ useTranslateableAttribute(step, "name") }}
            <AlertTriangle
                v-if="step.hasErrors"
                class="text-danger ms-2"
                :size="20"
            />
        </h3>

        <OverviewStep :step="step" />

        <div
            v-for="substep in step.substeps"
            :key="substep.stepId"
            class="ms-3 mb-3 mt-3"
        >
            <h4 class="d-flex align-items-center">
                {{ useTranslateableAttribute(substep, "name") }}
                <AlertTriangle
                    v-if="substep.hasErrors"
                    class="text-danger ms-2"
                    :size="18"
                />
            </h4>
            <OverviewStep :step="substep" />
        </div>
    </div>
</template>
