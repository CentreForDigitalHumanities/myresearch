<script lang="ts" setup>
import type { FileUploadQuestionWithValue } from "~/composables/useProcessForm";
import FormLabel from "./FormLabel.vue";

interface Props {
    question: FileUploadQuestionWithValue;
    isInvalid: boolean;
}

defineProps<Props>();

const modelValue = defineModel<number | null>();

const config = useRuntimeConfig();
const uploadUrl = `${config.public.API_URL}/form/upload/`;

// Local state for display purposes (file name, size) and for building the download URL
const currentFile = ref<{ name: string; size: number } | null>(null);
const fileUuid = ref<string | null>(null);

const isUploading = ref(false);
const uploadError = ref<string | null>(null);

async function onFileChanged(event: Event) {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];
    if (!file) {
        return;
    }

    isUploading.value = true;
    uploadError.value = null;

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await $fetch<{ value: number; uuid: string }>(
            uploadUrl,
            {
                method: "POST",
                body: formData,
                credentials: "include",
            },
        );
        modelValue.value = response.value;
        fileUuid.value = response.uuid;
        currentFile.value = { name: file.name, size: file.size };
    } catch {
        uploadError.value = "Upload failed. Please try again.";
        modelValue.value = null;
        fileUuid.value = null;
        currentFile.value = null;
    } finally {
        isUploading.value = false;
    }
}

function removeFile() {
    modelValue.value = null;
    fileUuid.value = null;
    currentFile.value = null;
    uploadError.value = null;
}

const downloadUrl = computed(() =>
    fileUuid.value
        ? `${config.public.API_URL}/form/files/${fileUuid.value}/`
        : null,
);
</script>

<template>
    <div>
        <FormLabel :question="question" />
        <p
            v-if="question.descriptionNl || question.descriptionEn"
            class="text-muted"
        >
            {{ useTranslateableAttribute(question, "description") }}
        </p>
        <input
            :id="`${question.questionId}-${question.repeatIndex}`"
            ref="fileInput"
            type="file"
            class="form-control"
            :class="{ 'is-invalid': isInvalid }"
            :disabled="isUploading"
            @change="onFileChanged($event)"
        />
        <div v-if="isUploading" class="mt-2 text-muted">
            {{ $t("Uploading…") }}
        </div>
        <div v-if="uploadError" class="mt-2 text-danger">
            {{ uploadError }}
        </div>
        <div v-if="currentFile" class="mt-2">
            <strong>{{ $t("Selected file") }}:</strong>
            {{ currentFile.name }} ({{
                (currentFile.size / (1024 * 1024)).toFixed(1)
            }}
            MB)
            <a
                v-if="downloadUrl"
                :href="downloadUrl"
                class="btn btn-outline-primary btn-sm ms-2"
                target="_blank"
            >
                {{ $t("Download") }}
            </a>
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
