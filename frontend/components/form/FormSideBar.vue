<script lang="ts" setup>
import { graphql, useFragment, type FragmentType } from "~/generated/gql";

const FormInfoFragment = graphql(`
    fragment FormInfoFragment on StepType {
        infoText {
            id
            textNl
            textEn
        }
    }
`);

const StepInfoFragment = graphql(`
    fragment StepInfoFragment on StepType {
        stepInfo {
            id
            textNl
            textEn
            contentNl
            contentEn
        }
    }
`);

const props = defineProps<{
    step: FragmentType<typeof StepInfoFragment>;
}>();

const stepInfo = computed(
    () => useFragment(StepInfoFragment, props.step).stepInfo,
);
</script>
<template>
    <div class="uu-form-help">
        <div v-if="stepInfo?.length !== 0" class="help-item">
            <strong>{{ $t("Additional Information") }}</strong>
            <div v-for="qa in stepInfo" :key="qa.id">
                <details>
                    <summary>
                        {{ useTranslateableAttribute(qa, "text") }}
                    </summary>
                    <div
                        v-html="useTranslateableAttribute(qa, 'content')"
                    ></div>
                </details>
            </div>
        </div>
    </div>
</template>

<style lang="scss" scoped>
.help-item:not(:last-child) {
    margin-bottom: 2rem;
}
</style>
