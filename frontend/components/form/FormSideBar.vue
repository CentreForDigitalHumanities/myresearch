<script lang="ts" setup>
import { graphql, useFragment, type FragmentType } from "~/generated/gql";
import { computed } from "vue";

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

const uniquePageAccordionKey = computed(() => "additionalInfo");
</script>
<template>
    <div v-if="stepInfo?.length !== 0">
        <strong>{{ $t("Additional Information") }}</strong>
        <div
            :id="'accordion' + uniquePageAccordionKey"
            class="accordion mw-100"
        >
            <div
                v-for="(info, index) in stepInfo"
                :key="uniquePageAccordionKey + index"
                class="mw-100"
            >
                <div class="accordion-item mw-100">
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
                        class="accordion-collapse collapse mw-100"
                        :data-bs-parent="'#accordion' + uniquePageAccordionKey"
                    >
                        <div class="accordion-body mw-100">
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

<style lang="scss" scoped></style>
