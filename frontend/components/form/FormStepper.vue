<script lang="ts" setup>
import { useTranslateableAttribute } from "../../composables/useLocalisation";
import type { FormStep, FormStepperConfig } from "./FormStepper";

interface Props {
    stepperConfig: FormStepperConfig;
}

const props = defineProps<Props>();
const emit = defineEmits<{
    (e: "step-clicked", slug: string): void;
}>();

function stepperItemClasses(step: FormStep): string {
    const classes: string[] = [
        "stepper-item",
        "bg-transparent",
        "border-0",
        "text-start",
        "m-0",
        "p-0",
    ];
    if (step.active) {
        classes.push("active");
    }
    if (step.completed) {
        classes.push("complete");
    }
    if (step.disabled) {
        classes.push("disabled");
    }
    return classes.join(" ");
}
</script>

<template>
    <div class="stepper-container">
        <div class="stepper">
            <ul>
                <li
                    v-for="(step, index) in props.stepperConfig.steps"
                    :key="`${step.slug}-${index}`"
                >
                    <button
                        type="button"
                        :class="stepperItemClasses(step)"
                        :disabled="step.disabled"
                        :aria-label="useTranslateableAttribute(step, 'label')"
                        @click="emit('step-clicked', step.slug)"
                    >
                        <span class="stepper-bubble stepper-bubble-largest">{{
                            index + 1
                        }}</span>
                        <span>{{
                            useTranslateableAttribute(step, "label")
                        }}</span>
                    </button>
                    <ul v-if="step.substeps.length > 0">
                        <li
                            v-for="(child, childIndex) in step.substeps"
                            :key="`${child.slug}-${childIndex}`"
                        >
                            <button
                                type="button"
                                :class="stepperItemClasses(child)"
                                :disabled="child.disabled"
                                :aria-label="
                                    useTranslateableAttribute(child, 'label')
                                "
                                @click="emit('step-clicked', child.slug)"
                            >
                                <span
                                    class="stepper-bubble stepper-bubble-medium"
                                ></span>
                                <span>{{
                                    useTranslateableAttribute(child, "label")
                                }}</span>
                            </button>
                        </li>
                    </ul>
                </li>
            </ul>
        </div>
    </div>
</template>
