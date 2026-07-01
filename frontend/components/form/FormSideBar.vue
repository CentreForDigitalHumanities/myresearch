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

const props = defineProps<{
    step: FragmentType<typeof FormInfoFragment>;
}>();

const stepInfo = computed(() => useFragment(FormInfoFragment, props.step));
</script>
<template>
    <div class="uu-form-help">
        <div class="help-item">
            <div v-if="stepInfo.infoText">
                <strong>{{ $t("Additional Information") }}</strong>
                <div
                    v-html="
                        useTranslateableAttribute(stepInfo.infoText, 'text')
                    "
                ></div>
            </div>
        </div>
    </div>
</template>

<style lang="scss" scoped>
.help-item:not(:last-child) {
    margin-bottom: 2rem;
}
</style>
