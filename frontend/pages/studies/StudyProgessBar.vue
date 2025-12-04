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

const Created: ProgressItem = {
	label: t("Created"),
	isActive: false,
	isComplete: true,
}

const NotYetSubmitted: ProgressItem = {
	label: t("Submitted"),
	isActive: true,
	isComplete: false,
}

const NotYetReviewed: ProgressItem = {
	label: t("Review from Privacy Officer"),
	isActive: false,
	isComplete: false,
}

const NotYetConcluded: ProgressItem = {
	label: t("Conclusion"),
	isActive: false,
	isComplete: false,
}

const DraftProgress: ProgressItem[] = [
	Created,
	NotYetSubmitted,
	NotYetReviewed,
	NotYetConcluded,
]

// Revision scenario

const Submitted: ProgressItem = {
	label: NotYetSubmitted.label,
	isActive: false,
	isComplete: true,
}

const Reviewed: ProgressItem = {
	label: NotYetReviewed.label,
	isActive: false,
	isComplete: true,
}

const RevisionCreated: ProgressItem = {
	label: t("Revision Created"),
	isActive: false,
	isComplete: true,
}

const ActiveReview: ProgressItem = {
	label: NotYetReviewed.label,
	isActive: true,
	isComplete: false,
}

const RevisionReviewProgress: ProgressItem[] = [
	Created,
	Submitted,
	Reviewed,
	RevisionCreated,
	Submitted,
	ActiveReview,
	NotYetConcluded,
]

const ProgressItems = computed(() =>
    props.studyStatus === "draft" ? DraftProgress : RevisionReviewProgress,
);

</script>

<template>
    <div class="stepper h-100">
        <ul class="h-100 d-flex flex-column justify-content-between">
            <li v-for="(progressItem, index) in ProgressItems" :key="index">
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
