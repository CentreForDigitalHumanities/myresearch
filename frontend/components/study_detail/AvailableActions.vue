<script setup lang="ts">
import { useI18n } from "vue-i18n";
import { useQuery } from "@vue/apollo-composable";
import { FileText, PencilLine, Send, Paperclip, Scale } from "lucide-vue-next";
import type { Component } from "vue";
import { graphql } from "~/generated/gql";
import type { GetFirstSlugQuery } from "~/generated/gql/graphql";

const props = defineProps<{
    studyStatus: string;
    submissionId: string | undefined;
}>();


// We only need to know the slug of the top-level form so we can link to it.
const GET_FIRST_SLUG = graphql(`
    query GetFirstSlug($submissionId: ID!) {
        form(submissionId: $submissionId) {
            formId
            steps {
                stepId
                slug
            }
        }
    }
`);

const queryVariables = computed(() => 
    props.submissionId ? { submissionId: props.submissionId } : null
);

const { result } = useQuery<GetFirstSlugQuery>(
    GET_FIRST_SLUG,
    queryVariables
);

const slug = computed<string | null>(() => {
    const firstStep = result.value?.form?.steps[0];
    return firstStep?.slug || null;
});

const continue_url = computed(() => 
    slug.value ? `/procreg/${props.submissionId}/${slug.value}` : ""
);

const { t } = useI18n();

type AvailableAction = {
    label: string;
    href: string;
    icon: Component;
};

// Some mock actions ...

// Draft actions

const draftActions = computed<AvailableAction[]>(() => [
  {
    label: t("Continue editing"),
    href: continue_url.value,
    icon: PencilLine,
  },
  {
    label: t("Submit"),
    href: "#",
    icon: Send,
  }
]);

// Actions for the PO

const POActions = computed<AvailableAction[]>(() => [
    {
        label: t("Continue editing"),
        href: continue_url.value,
        icon: PencilLine,
    },
    {
    label: t("View attachments"),
    href: "#",
    icon: Paperclip,
    },
    {
    label: t("Submit decision"),
    href: "#",
    icon: Scale,
    }
]);

const availableActions = computed(() =>
    props.studyStatus === "draft" ? draftActions.value : POActions.value,
);
</script>

<template>
    <h3 class="mb-3">{{ $t("Available actions") }}:</h3>
    <div class="tiles">
        <a
            v-for="(action, index) in availableActions"
            :key="index"
            :href="action.href"
            class="tile h-100 justify-content-around"
        >
            <strong class="text-center">{{ $t(action.label) }}</strong>
            <component :is="action.icon">            
            </component>
        </a>
    </div>
</template>
