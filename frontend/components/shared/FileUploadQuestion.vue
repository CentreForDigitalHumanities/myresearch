<script lang="ts" setup>
import type { FileUploadQuestionWithValue } from "~/composables/useProcessForm";

interface Props {
    question: FileUploadQuestionWithValue;
    isInvalid: boolean;
}

interface Emits {
    (e: "update:modelValue", value: File | null): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const currentFile = ref<File | null>(props.question.value);
const fileInput = ref<HTMLInputElement | null>(null);

function onFileChanged(event: Event) {
    const target = event.target as HTMLInputElement;
    if (target.files) {
        currentFile.value = target.files[0];
    } else {
        currentFile.value = null;
    }
    updateModelValue();
}

function removeFile(): void {
    currentFile.value = null;
    updateModelValue();

    // Update the input control to reflect the removal.
    if (fileInput.value) {
        fileInput.value.value = "";
    }
}

function updateModelValue(): void {
    emit("update:modelValue", currentFile.value);
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
        <div v-if="currentFile" class="mt-2">
            <strong>{{ $t("Selected file") }}:</strong>
            {{ currentFile.name }} ({{
                (currentFile.size / (1024 * 1024)).toFixed(1)
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
