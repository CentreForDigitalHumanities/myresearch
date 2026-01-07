<script lang="ts" setup>
import { graphql, useFragment, type FragmentType } from "~/generated/gql";

const FormInfoFragment = graphql(`
    fragment FormInfoFragment on StepType {
        infoQuestions {
            id
            textNl
            textEn
            link
        }
        infoTexts {
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
            <div v-if="stepInfo.infoQuestions?.length">
                <strong>{{ $t("Questions?") }}</strong>
            </div>
            <template
                v-for="(question, index) in stepInfo.infoQuestions"
                :key="index"
            >
                <a
                    :href="question.link"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="d-block my-1"
                >
                    {{ useTranslateableAttribute(question, "text") }}
                </a>
            </template>
        </div>
        <div class="help-item">
            <div v-if="stepInfo.infoTexts?.length">
                <strong>{{ $t("Additional Information") }}</strong>
                <ul>
                    <li
                        v-for="(info, index) in stepInfo.infoTexts"
                        :key="index"
                    >
                        {{ useTranslateableAttribute(info, "text") }}
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<style lang="scss" scoped>
.help-item:not(:last-child) {
    margin-bottom: 2rem;
}
</style>
