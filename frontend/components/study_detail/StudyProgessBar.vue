<script setup lang="ts">
import { useI18n } from 'vue-i18n';

const props = defineProps<{
    studyStatus: string;
}>();

const { t } = useI18n();

type ProgressItem = {
	label: string;
	isActive: boolean;
	isComplete: boolean;
}

// draft scenario

const created: ProgressItem = {
	label: t("Created"),
	isActive: false,
	isComplete: true,
}

const notYetSubmitted: ProgressItem = {
	label: t("Submitted"),
	isActive: true,
	isComplete: false,
}

const notYetReviewed: ProgressItem = {
	label: t("Review from Privacy Officer"),
	isActive: false,
	isComplete: false,
}

const notYetConcluded: ProgressItem = {
	label: t("Conclusion"),
	isActive: false,
	isComplete: false,
}

const draftProgress: ProgressItem[] = [
	created,
	notYetSubmitted,
	notYetReviewed,
	notYetConcluded,
]

// Revision scenario

const submitted: ProgressItem = {
	label: notYetSubmitted.label,
	isActive: false,
	isComplete: true,
}

const reviewed: ProgressItem = {
	label: notYetReviewed.label,
	isActive: false,
	isComplete: true,
}

const revisionCreated: ProgressItem = {
	label: t("Revision Created"),
	isActive: false,
	isComplete: true,
}

const activeReview: ProgressItem = {
	label: notYetReviewed.label,
	isActive: true,
	isComplete: false,
}

const revisionReviewProgress: ProgressItem[] = [
	created,
	submitted,
	reviewed,
	revisionCreated,
	submitted,
	activeReview,
	notYetConcluded,
]

const progressItems = computed(() =>
    props.studyStatus === "draft" ? draftProgress : revisionReviewProgress,
);

</script>

<template>
    <div class="stepper h-100">
        <ul class="h-100 d-flex flex-column justify-content-between">
            <li v-for="(progressItem, index) in progressItems" :key="index">
                <a class="stepper-item disabled" v-bind:class="{ active: progressItem.isActive }">
                    <span
                        class="stepper-bubble stepper-bubble-largest" v-bind:class="{ complete: progressItem.isComplete, incomplete: !progressItem.isComplete && progressItem.isActive }"
                    ></span>
                    <span class="lh-1">{{ $t(progressItem.label) }}</span>
                </a>
            </li>
        </ul>
    </div>
</template>
