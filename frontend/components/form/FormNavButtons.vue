<script lang="ts" setup>
import { BSButton } from "cdh-vue-lib";
import { Send } from "lucide-vue-next";

interface Props {
    selectedStep: CombinedStepWithValues;
    allSteps: CombinedStepWithValues[];
    disableSubmit?: boolean;
    isOverview?: boolean;
}

type Emits = {
    (e: "navigate-to-slug", slug: string): void;
    (e: "final-submit"): void;
};

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const navigableSteps = computed(() =>
    props.allSteps.filter((step) => !step.isRepeatable),
);

// The step containing the RepeatableStepQuestion that controls the selected repeatable step
const repeatableParentStep = computed(() => {
    const step = props.selectedStep;
    const stepRepeatIndex = step.repeatIndex ?? null;
    if (!step.isRepeatable || !stepRepeatIndex) {
        return null;
    }
    return (
        props.allSteps.find((candidate) =>
            candidate.questions.some(
                (question) =>
                    question.__typename === "RepeatableStepQuestionType" &&
                    question.value.includes(stepRepeatIndex),
            ),
        ) ?? null
    );
});

const firstStepSelected = computed(() => {
    const selected = props.selectedStep;
    const steps = props.allSteps;
    return steps.at(0)?.slug === selected.slug;
});

const lastStepSelected = computed(() => {
    const selected = props.selectedStep;
    const steps = props.allSteps;
    return steps.at(-1)?.slug === selected.slug;
});

function findCurrentStepIndex(): number {
    return navigableSteps.value.findIndex(
        (step) => step.slug === props.selectedStep.slug,
    );
}

function getAdjacentStepSlug(offset: 1 | -1): string {
    const index = findCurrentStepIndex();
    const target = navigableSteps.value.at(index + offset);
    if (!target) {
        return props.selectedStep.slug;
    }
    return target.slug;
}

function getNextStepSlug(): string {
    return getAdjacentStepSlug(1);
}

function getPreviousStepSlug(): string {
    return getAdjacentStepSlug(-1);
}

function navigateToSlug(slug: string): void {
    emit("navigate-to-slug", slug);
}

const showPrevious = computed(() => {
    return !props.selectedStep.isRepeatable && !firstStepSelected.value;
});
const showNext = computed(() => {
    return !props.selectedStep.isRepeatable && !lastStepSelected.value;
});
const showSave = computed(() => {
    return !!repeatableParentStep.value;
});
const showSubmit = computed(() => {
    return props.selectedStep.isOverview;
});
</script>

<template>
    <div class="btn-group">
        <BSButton
            v-if="showPrevious"
            variant="primary"
            class="btn-arrow-left"
            @click="navigateToSlug(getPreviousStepSlug())"
        >
            {{ $t("Previous") }}
        </BSButton>
        <BSButton
            v-if="showNext"
            variant="primary"
            class="btn-arrow-right"
            @click="navigateToSlug(getNextStepSlug())"
        >
            {{ $t("Next") }}
        </BSButton>
        <BSButton
            v-if="repeatableParentStep && showSave"
            variant="primary"
            class="btn-arrow-left"
            @click="navigateToSlug(repeatableParentStep.slug)"
        >
            {{ $t("Save") }}
        </BSButton>
        <BSButton
            v-if="showSubmit"
            :disabled="disableSubmit"
            :variant="disableSubmit ? 'light' : 'success'"
            @click="emit('final-submit')"
        >
            {{ $t("Submit") }}
            <Send class="ms-2" :size="16" />
        </BSButton>
    </div>
</template>
