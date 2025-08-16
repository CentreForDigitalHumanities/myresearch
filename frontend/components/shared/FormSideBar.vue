<script lang="ts" setup>
import { graphql, useFragment, type FragmentType } from "~/generated/gql";

const StepInfoFragment = graphql(`
    fragment StepInfoFragment on StepInfoType {
        id
        questions {
            id
            textNl
            textEn
            link
        }
        texts {
            id
            textNl
            textEn
        }
    }
`);

const props = defineProps<{
    config: FragmentType<typeof StepInfoFragment>;
}>();

const infoConfig = computed(() => useFragment(StepInfoFragment, props.config));

</script>
<template>
    <div class="uu-form-help">
        <div class="help-item">
            <div v-if="infoConfig.questions?.length">
                <strong>{{ $t("Questions?") }}</strong>
            </div>
            <template
                v-for="(question, index) in infoConfig.questions"
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
            <div v-if="infoConfig.texts?.length">
                <strong>{{ $t("Additional Information") }}</strong>
                <ul>
                    <li
                        v-for="(info, index) in infoConfig.texts"
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
