<script setup lang="ts">
import { useMutation } from "@vue/apollo-composable";
import { graphql } from "~/generated/gql";

const router = useRouter();

// Define the CreateStudy mutation
const createStudyMutation = graphql(`
    mutation CreateNewStudy {
        createStudy {
            study {
                id
                title
            }
            errors {
                field
                messages
            }
        }
    }
`);

// Setup the mutation
const { mutate: createStudy, loading } = useMutation(createStudyMutation);

// Handle button click
const handleCreateStudy = async () => {
    try {
        const result = await createStudy();

        if (!result?.data) {
            useNotification("No response from server", "danger");
            return;
        }

        if (
            result.data.createStudy?.errors &&
            result.data.createStudy.errors.length > 0
        ) {
            useNotification(
                result.data.createStudy.errors[0].messages?.[0] ||
                    "Failed to create study",
                "danger",
            );
            return;
        }

        if (result.data.createStudy?.study?.id) {
            useNotification("Study created successfully", "success");
            // Redirect to the study detail page
            router.push(`/studies/${result.data.createStudy.study.id}`);
        }
    } catch (error) {
        console.error("Error creating study:", error);
        useNotification("Failed to create study. Please try again.", "danger");
    }
};
</script>
<template>
    <div class="uu-content">
        <div class="uu-hero">
            <h1>{{ $t("Start new registration") }}</h1>
        </div>
        <div class="uu-container">
            <p>
                {{
                    $t(
                        `You are about to register a new study. If you click on the button below, a new study will be created and you will be able to fill in a form.`,
                    )
                }}
            </p>
            <div class="w-100"></div>
            <button
                @click="handleCreateStudy"
                :disabled="loading"
                class="btn btn-primary btn-lg"
            >
                <span
                    v-if="loading"
                    class="spinner-border spinner-border-sm me-2"
                ></span>
                {{ loading ? $t("Creating...") : $t("Register new study") }} >>
            </button>
        </div>
    </div>
</template>
