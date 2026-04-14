<script lang="ts" setup>
import type { FormWithValues } from "~/composables/useProcessForm";
import OverviewStep from "./OverviewStep.vue";
import { AlertTriangle } from "lucide-vue-next";
import type { Validation } from "@vuelidate/core";

interface Props {
    form: FormWithValues;
    vuelidate: Validation;
}

const props = defineProps<Props>();

// Filter out the overview step itself.
const contentSteps = computed(() =>
    props.form.steps.filter((step) => !step.isOverview),
);
</script>

<template>
    <div v-for="step in contentSteps" :key="step.stepId" class="mb-4 p-2">
        <h3>{{ useTranslateableAttribute(step, "name") }}</h3>

        <div v-for="step in contentSteps" :key="step.stepId" class="mb-4 p-2">
            <h3>
                {{ useTranslateableAttribute(step, "name") }}
                <AlertTriangle
                    v-if="useStepHasErrors(vuelidate, step)"
                    class="warning-icon text-danger ms-2"
                    :size="20"
                />
            </h3>

            <div v-if="!step.substeps || step.substeps.length === 0">
                <OverviewStep :step="step" :vuelidate="vuelidate" />
            </div>

            <div v-else>
                <div
                    v-for="substep in step.substeps"
                    :key="substep.stepId"
                    class="ms-3 mb-3"
                >
                    <h4>
                        {{ useTranslateableAttribute(substep, "name") }}
                        <AlertTriangle
                            v-if="useStepHasErrors(vuelidate, substep)"
                            class="text-danger ms-2"
                            :size="18"
                        />
                    </h4>
                    <OverviewStep :step="substep" :vuelidate="vuelidate" />
                </div>
            </div>
        </div>
    </div>
</template>
