<script setup lang="ts">
import { useI18n } from "vue-i18n";
import { useQuery } from "@vue/apollo-composable";
import { PencilLine, Delete } from "lucide-vue-next";
import type { Component } from "vue";
import { graphql } from "~/generated/gql";
import type { GetFirstSlugQuery } from "~/generated/gql/graphql";
import Loading from "~/components/shared/Loading.vue";
import { StudyActionEnum } from "~/generated/gql/graphql";

const props = defineProps<{
  studyId: string;
  submissionId: string;
  actions: StudyActionEnum[];
}>();

// We need to know the slug of the top-level form so we can link to it.
const GET_FIRST_SLUG = graphql(`
  query GetFirstSlug($submissionId: ID!) {
    form(submissionId: $submissionId, mrPermission: "Edit") {
      formId
      steps {
        stepId
        slug
      }
    }
  }
`);

const { result } = useQuery<GetFirstSlugQuery>(GET_FIRST_SLUG, () => ({
  submissionId: props.submissionId,
}));

const slug = computed<string | null>(() => {
  const firstStep = result.value?.form?.steps[0];
  return firstStep?.slug || null;
});

const isSlugLoaded = computed(() => slug.value !== null);

const { t } = useI18n();

type AvailableAction = {
  label: string;
  name: string;
  params: Record<string, any>;
  icon?: Component;
  style?: Record<string, string>;
};

const handleActionClick = (action: AvailableAction) => {
  navigateTo({ name: action.name, params: action.params });
};

// NOTE: ensure that the strings used as keys here correspond with
// the strings we receive from the backend
const actionMap = computed<Record<StudyActionEnum, AvailableAction>>(() => ({
  [StudyActionEnum.EditAction]: {
    label: t("Continue editing"),
    name: "procreg-submissionId-slug",
    params: { submissionId: props.submissionId, slug: slug.value },
    icon: PencilLine,
  },
  [StudyActionEnum.DeleteAction]: {
    label: t("Delete"),
    name: "studies-studyId-delete",
    params: { studyId: props.studyId },
    icon: Delete,
    style: {
      "--bs-tiles-hover-bg": "var(--bs-danger)",
      "--bs-tiles-hover-color": "var(--bs-white)",
    },
  },
}));

const availableActions = computed<AvailableAction[]>(() =>
  props.actions.map((actionEnum) => actionMap.value[actionEnum]),
);
</script>

<template>
  <div v-if="!isSlugLoaded">
    <loading />
  </div>
  <div v-else-if="availableActions.length > 0">
    <h3 class="mb-3">{{ $t("Available actions") }}:</h3>
    <div class="tiles">
      <a
        v-for="(action, index) in availableActions"
        :key="index"
        @click.prevent="handleActionClick(action)"
        :style="action.style"
        class="tile h-100 justify-content-around"
      >
        <strong class="text-center">{{ $t(action.label) }}</strong>
        <component :is="action.icon"> </component>
      </a>
    </div>
  </div>
  <h3 v-else>{{ $t("No actions available") }}</h3>
</template>
