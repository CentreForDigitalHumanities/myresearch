<script lang="ts" setup>
import { BSIcon, useConfirm } from "cdh-vue-lib";
import useStaticFile from "~/composables/useStaticFile";
import { useMutation } from "@vue/apollo-composable";
import { graphql } from "~/generated/gql";
import { useI18n } from "vue-i18n";

const currentUser = computed(() => useCurrentUserStore().currentUser);

const { t } = useI18n();

const CREATE_STUDY_MUTATION = graphql(`
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

const { mutate: createStudy } = useMutation(CREATE_STUDY_MUTATION);

const handleCreateStudy = async () => {
    try {
        const result = await createStudy();

        if (!result?.data) {
            useNotification("No response from server", "danger");
            return;
        }

        if (result.data.createStudy?.errors?.length) {
            useNotification("Failed to create study", "danger");
            return;
        }

        if (result.data.createStudy?.study?.id) {
            useNotification("Study created successfully", "success");
            // Redirect to the study detail page
            void navigateTo(`/studies/${result.data.createStudy.study.id}`);
        }
    } catch {
        useNotification("Failed to create study. Please try again.", "danger");
    }
};

function newRegistration(): void {
    useConfirm({
        text: t("Are you sure you want to start a new registration?"),
        callback: () => {
            void handleCreateStudy();
        },
    });
}
</script>

<template>
    <nav
        class="navbar uu-navbar"
        role="navigation"
        aria-label="main navigation"
    >
        <div class="uu-navbar-container">
            <div class="navbar-brand">
                <img
                    alt="Utrecht University"
                    :src="useStaticFile('/images/logo-header-nl.svg')"
                />
            </div>
            <button
                class="navbar-toggler"
                type="button"
                data-bs-toggle="collapse"
                data-bs-target="#navbar-content"
                aria-expanded="false"
                aria-label="Toggle navigation"
            >
                <span class="navbar-toggler-icon" />
            </button>
            <div id="navbar-content" class="collapse navbar-collapse">
                <ul class="navbar-nav me-auto">
                    <li>
                        <NuxtLink to="/" class="nav-link" active-class="active">
                            <BSIcon icon="house" />
                        </NuxtLink>
                    </li>
                    <li>
                        <button class="nav-link" @click="newRegistration">
                            {{ $t("New registration") }}
                        </button>
                    </li>
                    <li v-if="currentUser">
                        <NuxtLink
                            to="/studies/"
                            class="nav-link"
                            active-class="active"
                        >
                            {{ $t("Studies") }}
                        </NuxtLink>
                    </li>
                </ul>
                <ul class="navbar-nav ms-auto">
                    <!-- Placeholder for items on the right -->
                </ul>
            </div>
        </div>
    </nav>
</template>
