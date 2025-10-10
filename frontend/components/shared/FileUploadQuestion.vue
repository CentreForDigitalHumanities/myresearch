<script lang="ts" setup>
import type { FileUploadQuestionWithValue } from "~/composables/useBuildForm";

interface Props {
    question: FileUploadQuestionWithValue;
    isInvalid: boolean;
}

interface Emits {
    (e: "update:modelValue", value: File | null): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const localQuestion = ref<File | null>(props.question.value);
const fileInput = ref<HTMLInputElement | null>(null);

function onFileChanged(event: Event) {
    const target = event.target as HTMLInputElement;
    if (target.files) {
        localQuestion.value = target.files[0];
    } else {
        localQuestion.value = null;
    }
    updateModelValue();
}

function removeFile(): void {
    localQuestion.value = null;
    updateModelValue();

    // Update the input control to reflect the removal.
    if (fileInput.value) {
        fileInput.value.value = "";
    }
}

function updateModelValue(): void {
    emit("update:modelValue", localQuestion.value);
}
</script>

<template>
    <div>
        <label :for="question.id" class="form-label">
            {{ useTranslateableAttribute(question, "text") }}
        </label>
        <p
            v-if="question.descriptionNl || question.descriptionEn"
            class="text-muted"
        >
            {{ useTranslateableAttribute(question, "description") }}
        </p>
        <input
            :id="question.id"
            ref="fileInput"
            type="file"
            class="form-control"
            :class="{ 'is-invalid': isInvalid }"
            @change="onFileChanged($event)"
        />
        <div v-if="localQuestion" class="mt-2">
            <strong>{{ $t("Selected file") }}:</strong>
            {{ localQuestion.name }} ({{
                (localQuestion.size / 1024).toFixed(2)
            }}
            KB)
            <button
                type="button"
                class="btn btn-outline-secondary btn-sm ms-2"
                @click="removeFile"
            >
                {{ $t("Remove") }}
            </button>
        </div>
    </div>
</template>
