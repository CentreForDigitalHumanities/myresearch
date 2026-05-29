<script lang="ts" setup>
import type {
    FileUploadAnswer,
    FileUploadQuestionWithValue,
} from "~/composables/useProcessForm";
import FormLabel from "./FormLabel.vue";
import { useDisplayFileSize } from "~/composables/useDisplayFileSize.js";
import { useI18n } from "vue-i18n";

interface Props {
    question: FileUploadQuestionWithValue;
    isInvalid: boolean;
}

const props = defineProps<Props>();

const modelValue = defineModel<FileUploadAnswer | null>({
    default: null,
});

// Initialize modelValue with an existing answer.
onMounted(() => (modelValue.value = props.question.value ?? null));

const { t } = useI18n();

const config = useRuntimeConfig();
const uploadUrl = `${config.public.API_URL}/form/upload/`;

const isUploading = ref(false);
const uploadError = ref<string | null>(null);

const downloadUrl = computed(() =>
    modelValue.value
        ? `${config.public.API_URL}/form/files/${modelValue.value.value}/`
        : null,
);

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
        const csrfToken = useCookie("csrftoken").value ?? "";
        const response = await $fetch<FileUploadAnswer>(uploadUrl, {
            method: "POST",
            body: formData,
            credentials: "include",
            headers: { "X-CSRFToken": csrfToken },
        });
        modelValue.value = response;
    } catch {
        uploadError.value = t("Upload failed. Please try again.");
        modelValue.value = null;
    } finally {
        isUploading.value = false;
    }
}

function removeFile() {
    modelValue.value = null;
    uploadError.value = null;
}
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
            v-show="!modelValue"
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
        <div v-if="modelValue" class="mt-2">
            <strong>{{ $t("Selected file") }}:</strong>
            {{ modelValue.name }} ({{ useDisplayFileSize(modelValue.size) }})
            <div class="d-flex">
                <button class="btn btn-primary btn-sm ms-2" role="button">
                    <a
                        v-if="downloadUrl"
                        class="text-decoration-none text-reset"
                        :href="downloadUrl"
                        download
                    >
                        {{ $t("Download") }}
                    </a>
                </button>
                <button
                    type="button"
                    class="btn btn-outline-secondary btn-sm ms-2"
                    @click="removeFile"
                >
                    {{ $t("Remove") }}
                </button>
            </div>
        </div>
    </div>
</template>
