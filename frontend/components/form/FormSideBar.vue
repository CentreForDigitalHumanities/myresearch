<script lang="ts" setup>
import { graphql, useFragment, type FragmentType } from "~/generated/gql";
import { computed } from "vue";

const StepInfoTextFragment = graphql(`
    fragment StepInfoTextFragment on StepType {
        stepInfoText {
            id
            textNl
            textEn
            contentNl
            contentEn
        }
    }
`);

const props = defineProps<{
    step: FragmentType<typeof StepInfoTextFragment>;
}>();

const stepInfoText = computed(
    () => useFragment(StepInfoTextFragment, props.step).stepInfoText,
);

const uniquePageAccordionKey = computed(() => "additionalInfo");
</script>
<template>
    <div v-if="stepInfoText?.length !== 0">
        <h4>{{ $t("Additional Information") }}</h4>
        <div :id="'accordion' + uniquePageAccordionKey" class="accordion">
            <div
                v-for="(info, index) in stepInfoText"
                :key="uniquePageAccordionKey + index"
            >
                <div class="accordion-item">
                    <h2 class="accordion-header">
                        <button
                            class="accordion-button"
                            type="button"
                            data-bs-toggle="collapse"
                            :data-bs-target="
                                '#collapse' + uniquePageAccordionKey + index
                            "
                            aria-expanded="false"
                            :aria-controls="
                                'collapse' + uniquePageAccordionKey + index
                            "
                        >
                            {{ useTranslateableAttribute(info, "text") }}
                        </button>
                    </h2>
                    <div
                        :id="'collapse' + uniquePageAccordionKey + index"
                        class="accordion-collapse collapse"
                        :data-bs-parent="'#accordion' + uniquePageAccordionKey"
                    >
                        <div class="accordion-body small-text">
                            <div
                                v-html="
                                    useTranslateableAttribute(info, 'content')
                                "
                            ></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style lang="scss" scoped>
.small-text {
    font-size: 0.9rem;
}
</style>
