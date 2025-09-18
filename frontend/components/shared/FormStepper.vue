<script lang="ts" setup>
import { useTranslateableAttribute } from "~/composables/useTranslation";

interface FormStep {
    slug: string;
    labelNl: string;
    labelEn: string;
    substeps: FormStep[];
    completed: boolean;
    active: boolean;
    disabled: boolean;
}

export interface FormStepperConfig {
    steps: Array<FormStep>;
}

interface Props {
    stepperConfig: FormStepperConfig;
}

const props = defineProps<Props>();

function stepperItemClasses(step: FormStep): string {
    const classes: string[] = ["stepper-item"];
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
                    <NuxtLink :class="stepperItemClasses(step)" :to="step.slug">
                        <span class="stepper-bubble stepper-bubble-largest">{{
                            index + 1
                        }}</span>
                        <span>{{
                            useTranslateableAttribute(step, "label")
                        }}</span>
                    </NuxtLink>
                    <ul v-if="step.substeps.length > 0">
                        <li
                            v-for="(child, childIndex) in step.substeps"
                            :key="`${child.slug}-${childIndex}`"
                        >
                            <NuxtLink
                                :class="stepperItemClasses(child)"
                                :to="child.slug"
                            >
                                <span
                                    class="stepper-bubble stepper-bubble-medium"
                                ></span>
                                <span>{{
                                    useTranslateableAttribute(child, "label")
                                }}</span>
                            </NuxtLink>
                        </li>
                    </ul>
                </li>
            </ul>
        </div>
    </div>
</template>
