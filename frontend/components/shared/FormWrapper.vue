<script lang="ts" setup>
import { computed } from "vue";
import { BSButton } from "cdh-vue-lib";
import FormStepper, { type FormStepperConfig } from "./FormStepper.vue";
import { type GetFormQuery } from "~/generated/gql/graphql";

export type TopLevelForm = NonNullable<GetFormQuery["form"]>;
export type Subform = NonNullable<TopLevelForm["subforms"][number]>;
export type NestedSubform = NonNullable<Subform["subforms"][number]>;

export type CombinedForm = TopLevelForm | Subform | NestedSubform;

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
        steps: topLevelForm.subforms.map((form) => ({
            slug: form.slug,
            labelNl: form.nameNl ?? "",
            labelEn: form.nameEn ?? "",
            completed: false,
            active: form.slug === selectedFormSlug,
            disabled: false,
            children: form.subforms.map((subform) => ({
                slug: subform.slug,
                labelNl: subform.nameNl ?? "",
                labelEn: subform.nameEn ?? "",
                completed: false,
                active: subform.slug === selectedFormSlug,
                disabled: false,
                // Let's only go 2 levels deep for now.
                children: [],
            })),
        })),
    };
});

const allForms = computed(() => getAllForms(props.form));
const selectedForm = computed(() => {
    const forms = allForms.value;
    if (forms.length <= 0) {
        return null;
    }
    return forms.find(({ slug }) => slug === props.currentFormSlug) ?? null;
});

function getAllForms(form: CombinedForm) {
    const collectedForms = [form];
    if ("subforms" in form) {
        form.subforms.forEach((subform) => {
            collectedForms.push(...getAllForms(subform));
        });
    }
    return collectedForms;
}

function findCurrentFormIndex(): number {
    const selectedFormValue = selectedForm.value;
    if (!selectedFormValue) {
        return -1;
    }

    const forms = allForms.value;
    return forms.findIndex((form) => form.slug === selectedFormValue.slug);
}

function getNextFormSlug(): string {
    if (!selectedForm.value) {
        return props.currentFormSlug;
    }

    const forms = allForms.value;
    const currentIndex = findCurrentFormIndex();

    if (currentIndex === -1 || currentIndex >= forms.length - 1) {
        // Already at the last form or form not found.
        return props.currentFormSlug;
    }

    return forms[currentIndex + 1].slug;
}

function getPreviousFormSlug(): string {
    if (!selectedForm.value) {
        return props.currentFormSlug;
    }

    const forms = allForms.value;
    const currentIndex = findCurrentFormIndex();

    if (currentIndex <= 0) {
        // Already at the first form or form not found.
        return props.currentFormSlug;
    }

    return forms[currentIndex - 1].slug;
}
</script>

<template>
    <div v-if="selectedForm" class="col-12 d-flex">
        <FormStepper
            class="col-3 d-lg-block d-none pe-2"
            :stepper-config="formStepperConfig"
            :selected-form-slug="props.currentFormSlug"
        />
        <div class="col-12 col-lg-9">
            <form class="uu-form">
                <SharedMRForm :form="selectedForm" />
            </form>
            <div class="btn-group">
                <NuxtLink
                    :to="{
                        name: 'procreg-slug',
                        params: { slug: getPreviousFormSlug() },
                    }"
                >
                    <BSButton variant="primary" class="btn-arrow-left">
                        {{ $t("Previous") }}
                    </BSButton>
                </NuxtLink>
                <NuxtLink
                    :to="{
                        name: 'procreg-slug',
                        params: { slug: getNextFormSlug() },
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
