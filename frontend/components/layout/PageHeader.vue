<script setup lang="ts">
import { BSIcon } from "cdh-vue-lib";
import { useI18n } from "vue-i18n";
import { useCurrentUserStore } from "~/stores/current-user";

const title = useAppConfig().globalTitle;
const i18n = useI18n();

function setLocale(locale: string) {
    i18n.locale.value = locale;
    localStorage.locale = locale;
}

const config = useRuntimeConfig();
const currentUserStore = useCurrentUserStore();
await callOnce("user", () => currentUserStore.loadData());

const loginUrl = computed(() => {
    const redirect = encodeURIComponent(window.location.href);
    return `${config.public.SAML_URL}/login/?next=${redirect}`;
});
const logoutUrl = computed(() => {
    // Current page may not be available after logout, so redirect to home page
    return `${config.public.SAML_URL}/logout/`;
});
</script>

<template>
    <div class="uu-header">
        <div class="uu-header-row">
            <div class="col-3">
                <img
                    alt="Utrecht University"
                    :src="useStaticFile('/images/logo-header-nl.svg')"
                    class="uu-logo"
                />
            </div>
            <div class="uu-header-title text-red col-6 justify-content-center">
                {{ title }}
            </div>
            <div class="ms-auto">
                <!-- Spacer element, moves the next elements to the right -->
            </div>
            <div
                v-if="currentUserStore.currentUser?.isStaff"
                class="border-left px-3"
            >
                <NuxtLink to="/" class="nav-link">
                    <BSIcon icon="gear" size="lg" />
                </NuxtLink>
            </div>
            <div
                v-if="$i18n.locale === 'nl'"
                class="language-switcher"
                @click="setLocale('en')"
            >
                English
            </div>
            <div
                v-if="$i18n.locale === 'en'"
                class="language-switcher"
                @click="setLocale('nl')"
            >
                Nederlands
            </div>
        </div>
        <div class="uu-header-row">
            <div v-if="currentUserStore.currentUser" class="ms-auto">
                {{
                    $t("Welcome, {name}", {
                        name: currentUserStore.currentUser?.fullName,
                    })
                }}
                (<a :href="logoutUrl" class="text-decoration-underline">{{
                    $t("Logout")
                }}</a
                >)
            </div>
            <div v-else class="ms-auto">
                <a :href="loginUrl" class="text-decoration-underline">{{
                    $t("Login")
                }}</a>
            </div>
        </div>
    </div>
</template>

<style scoped lang="scss">
@use "uu-bootstrap/scss/configuration";
.header-breadcrumbs {
    --bs-breadcrumb-margin-bottom: 0;

    .active {
        color: configuration.$text-muted;
    }
}

.language-switcher {
    cursor: pointer;
    color: configuration.$text-muted;
    text-transform: uppercase;
    border-left: 1px solid configuration.$border-color;
    padding-left: 1rem;
    user-select: none;
}

.uu-logo {
    height: 50px;
}
</style>
