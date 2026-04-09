<script setup lang="ts">
import { useI18n } from "vue-i18n";
import { FileText, PencilLine, Send, Paperclip, Scale } from "lucide-vue-next";
import type { Component } from "vue";

const props = defineProps<{
  studyStatus: string;
}>();

const { t } = useI18n();

type AvailableAction = {
  label: string;
  href: string;
  icon: Component;
};

// Some mock actions ...

// Draft actions

const draftActions: AvailableAction[] = [
  {
    label: t("Continue editing"),
    href: "#",
    icon: PencilLine,
  },
  {
    label: t("Submit"),
    href: "#",
    icon: Send,
  },
];

// Actions for the PO

const POActions: AvailableAction[] = [
  {
    label: t("View PDF"),
    href: "#",
    icon: FileText,
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
  },
];

const availableActions = computed(() =>
  props.studyStatus === "draft" ? draftActions : POActions,
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
      <component :is="action.icon"> </component>
    </a>
  </div>
</template>
