<script lang="ts" setup>
import { computed } from "vue";
import { BSButton } from "cdh-vue-lib";
import FormStepper, { type FormStepperConfig } from "./FormStepper.vue";
import { type GetFormQuery } from "~/generated/gql/graphql";

export type QueriedForm = NonNullable<GetFormQuery["form"]>;
export type Step = NonNullable<QueriedForm["steps"][number]>;
export type Substep = NonNullable<Step["substeps"][number]>;

export type CombinedStep = Step | Substep;

interface Props {
    form: NonNullable<GetFormQuery["form"]>;
    currentFormSlug: string;
}

const props = defineProps<Props>();

const formStepperConfig = computed<FormStepperConfig>(() => {
    const selectedFormSlug = props.currentFormSlug;

    const topLevelForm = props.form;

    return {
        titleNl: topLevelForm.nameNl ?? "",
        titleEn: topLevelForm.nameEn ?? "",
        steps: topLevelForm.steps.map((step) => ({
            slug: step.slug,
            labelNl: step.nameNl ?? "",
            labelEn: step.nameEn ?? "",
            completed: false,
            active: step.slug === selectedFormSlug,
            disabled: false,
            children: step.substeps.map((substep) => ({
                slug: substep.slug,
                labelNl: substep.nameNl ?? "",
                labelEn: substep.nameEn ?? "",
                completed: false,
                active: substep.slug === selectedFormSlug,
                disabled: false,
                // Let's only go 2 levels deep for now.
                children: [],
            })),
        })),
    };
});

const allSteps = computed(() => getAllSteps(props.form));
const selectedStep = computed(() => {
    const steps = allSteps.value;
    if (steps.length <= 0) {
        return null;
    }
    return steps.find(({ slug }) => slug === props.currentFormSlug) ?? null;
});

function getAllSteps(form: QueriedForm): CombinedStep[] {
    const collectedSteps: CombinedStep[] = form.steps;
    form.steps.forEach((step) => {
        if ("substeps" in step) {
            collectedSteps.push(...step.substeps);
        }
    });
    return collectedSteps;
}

function findCurrentStepIndex(): number {
    const selectedStepValue = selectedStep.value;
    if (!selectedStepValue) {
        return -1;
    }

    const steps = allSteps.value;
    return steps.findIndex((step) => step.slug === selectedStepValue.slug);
}

function getNextStepSlug(): string {
    if (!selectedStep.value) {
        return props.currentFormSlug;
    }

    const steps = allSteps.value;
    const currentIndex = findCurrentStepIndex();

    if (currentIndex === -1 || currentIndex >= steps.length - 1) {
        // Already at the last step or step not found.
        return props.currentFormSlug;
    }

    return steps[currentIndex + 1].slug;
}

function getPreviousStepSlug(): string {
    if (!selectedStep.value) {
        return props.currentFormSlug;
    }

    const steps = allSteps.value;
    const currentIndex = findCurrentStepIndex();

    if (currentIndex <= 0) {
        // Already at the first step or step not found.
        return props.currentFormSlug;
    }

    return steps[currentIndex - 1].slug;
}
</script>

<template>
    <div v-if="selectedStep" class="col-12 d-flex">
        <FormStepper
            class="col-3 d-lg-block d-none pe-2"
            :stepper-config="formStepperConfig"
            :selected-form-slug="props.currentFormSlug"
        />
        <div class="col-12 col-lg-9">
            <form class="uu-form">
                <SharedMRForm :form="selectedStep" />
            </form>
            <div class="btn-group">
                <NuxtLink
                    :to="{
                        name: 'procreg-slug',
                        params: { slug: getPreviousStepSlug() },
                    }"
                >
                    <BSButton variant="primary" class="btn-arrow-left">
                        {{ $t("Previous") }}
                    </BSButton>
                </NuxtLink>
                <NuxtLink
                    :to="{
                        name: 'procreg-slug',
                        params: { slug: getNextStepSlug() },
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
