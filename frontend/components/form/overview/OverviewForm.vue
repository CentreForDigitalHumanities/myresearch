<script lang="ts" setup>
import type { FormWithValues } from "~/composables/useProcessForm";
import OverviewStep from "./OverviewStep.vue";

interface Props {
    form: FormWithValues;
}

const props = defineProps<Props>();

// Filter out the overview step itself.
const contentSteps = computed(() =>
    props.form.steps.filter((step) => step.stepId !== "overview-step-id"),
);
</script>

<template>
    <div>
        <h2>{{ $t("Submission overview") }}</h2>
        <p>
            {{
                $t(
                    "Please review your answers below and return to previous steps to make any necessary changes. When you are ready to submit, click the 'Submit' button.",
                )
            }}
        </p>

        <div v-for="step in contentSteps" :key="step.stepId" class="mb-4 p-2">
            <h3>{{ useTranslateableAttribute(step, "name") }}</h3>

            <div v-if="!step.substeps || step.substeps.length === 0">
                <OverviewStep :step="step" />
            </div>

            <div v-else>
                <div
                    v-for="substep in step.substeps"
                    :key="substep.stepId"
                    class="ms-3 mb-3"
                >
                    <h4>{{ useTranslateableAttribute(substep, "name") }}</h4>
                    <OverviewStep :step="substep" />
                </div>
            </div>
        </div>
    </div>
</template>
