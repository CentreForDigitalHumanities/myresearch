<script lang="ts" setup>
import type { FormWithValues } from "~/composables/useProcessForm";
import OverviewStep from "./OverviewStep.vue";
import { AlertTriangle } from "lucide-vue-next";
import type { Validation } from "@vuelidate/core";
import { useStepHasErrors } from "~/composables/useFormErrors";

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
        <h3 class="d-flex align-items-center">
            {{ useTranslateableAttribute(step, "name") }}
            <AlertTriangle
                v-if="useStepHasErrors(vuelidate, step)"
                class="text-danger ms-2"
                :size="20"
            />
        </h3>

        <OverviewStep :step="step" :vuelidate="vuelidate" />

        <div
            v-for="substep in step.substeps"
            :key="substep.stepId"
            class="ms-3 mb-3"
        >
            <h4 class="d-flex align-items-center">
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
</template>
