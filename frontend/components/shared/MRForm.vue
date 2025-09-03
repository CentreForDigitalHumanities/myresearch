<script lang="ts" setup>
import { ref, computed } from "vue";
import { BSButton } from "cdh-vue-lib";
import FormStepper, { type FormStepperConfig } from "./FormStepper.vue";
import { type GetFormQuery } from "~/generated/gql/graphql";

type QueriedForm = NonNullable<GetFormQuery["form"]>;
type ParentStep = NonNullable<QueriedForm["steps"][number]>;
type Substep = NonNullable<ParentStep["substeps"][number]>;

export type Step = ParentStep | Substep;

interface Props {
    form: QueriedForm;
    currentStepSlug: string;
}

const props = defineProps<Props>();

const steps = computed<ParentStep[]>(() =>
    props.form.steps.map((step) => ({
        ...step,
        substeps: step.substeps.map((substep) => ({
            ...substep,
        })),
    })),
);

const formStepperConfig = computed<FormStepperConfig>(() => {
    const selectedStepSlug = selectedStep.value?.slug;

    return {
        titleNl: props.form.nameNl ?? "",
        titleEn: props.form.nameEn ?? "",
        steps: steps.value.map((step) => ({
            slug: step.slug,
            labelNl: step.nameNl ?? "",
            labelEn: step.nameEn ?? "",
            completed: false,
            active: step.slug === selectedStepSlug,
            disabled: false,
            children: step.substeps.map((substep) => ({
                slug: substep.slug,
                labelNl: substep.nameNl ?? "",
                labelEn: substep.nameEn ?? "",
                completed: false,
                active: substep.slug === selectedStepSlug,
                disabled: false,
                children: [],
            })),
        })),
    };
});



const selectedStep = ref<Step | null>(defaultStep());

function getAllSteps(): Step[] {
    const allSteps: Step[] = [];

    steps.value.forEach((step) => {
        // Add main step.
        allSteps.push(step);

        if (step.substeps.length === 0) {
            return;
        }

        // Add substeps sorted by order.
        const sortedSubsteps: Substep[] = [...step.substeps].sort(
            (a, b) => (a.parentOrder ?? 0) - (b.parentOrder ?? 0),
        );
        allSteps.push(...sortedSubsteps);
    });

    return allSteps;
}

function defaultStep(): Step | null {
    const allSteps = getAllSteps();
    if (allSteps.length <= 0) {
        return null;
    }
    return allSteps.find(({ slug }) => slug === props.currentStepSlug) ?? null;
}

function findCurrentStepIndex(): number {
    const selectedStepValue = selectedStep.value;
    if (!selectedStepValue) {
        return -1;
    }

    const allSteps = getAllSteps();
    return allSteps.findIndex((step) => step.slug === selectedStepValue.slug);
}

function getNextStepSlug(): string {
    if (!selectedStep.value) {
        return props.currentStepSlug;
    }

    const allSteps = getAllSteps();
    const currentIndex = findCurrentStepIndex();

    if (currentIndex === -1 || currentIndex >= allSteps.length - 1) {
        // Already at the last step or step not found.
        return props.currentStepSlug;
    }

    return allSteps[currentIndex + 1].slug;
}

function getPreviousStepSlug(): string {
    if (!selectedStep.value) {
        return props.currentStepSlug;
    }

    const allSteps = getAllSteps();
    const currentIndex = findCurrentStepIndex();

    if (currentIndex <= 0) {
        // Already at the first step or step not found.
        return props.currentStepSlug;
    }

    return allSteps[currentIndex - 1].slug;
}
</script>

<template>
    <div v-if="selectedStep" class="col-12 d-flex">
        <FormStepper
            class="col-2 d-lg-block d-none"
            :step-config="formStepperConfig"
            :selected-step="props.currentStepSlug"
        />
        <div class="col-12 col-lg-10">
            <form class="uu-form">
                <SharedFormStep :step="selectedStep" />
            </form>
            <div class="btn-group">
                <NuxtLink
                    :to="{
                        name: 'procreg-step',
                        params: { step: getPreviousStepSlug() },
                    }"
                >
                    <BSButton variant="primary" class="btn-arrow-left">
                        {{ $t("Previous") }}
                    </BSButton>
                </NuxtLink>
                <NuxtLink
                    :to="{
                        name: 'procreg-step',
                        params: { step: getNextStepSlug() },
                    }"
                >
                    <BSButton variant="primary" class="btn-arrow-right">
                        {{ $t("Next") }}
                    </BSButton>
                </NuxtLink>
            </div>
        </div>
    </div>
</template>
