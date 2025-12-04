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

const Continue: AvailableAction = {
    label: t("Continue editing"),
    href: "#",
    icon: PencilLine,
};

const Submit: AvailableAction = {
    label: t("Submit"),
    href: "#",
    icon: Send,
};

const DraftActions: AvailableAction[] = [Continue, Submit];

// Actions for the PO

const ViewPDF: AvailableAction = {
    label: t("View PDF"),
    href: "#",
    icon: FileText,
};

const ViewAttachments: AvailableAction = {
    label: t("View attachments"),
    href: "#",
    icon: Paperclip,
};

const SubmitDecision: AvailableAction = {
    label: t("Submit decision"),
    href: "#",
    icon: Scale,
};

const POActions: AvailableAction[] = [ViewPDF, ViewAttachments, SubmitDecision];

const AvailableActions = computed(() =>
    props.studyStatus === "draft" ? DraftActions : POActions,
);
</script>

<template>
    <h3 class="mb-3">Available actions:</h3>
    <div class="tiles">
        <a
            v-for="(action, index) in AvailableActions"
            :key="index"
            :href="action.href"
            class="tile h-100 justify-content-around"
        >
            <strong class="text-center">{{ $t(action.label) }}</strong>
            <component :is="action.icon" class="icon">            
            </component>
        </a>
    </div>
</template>
