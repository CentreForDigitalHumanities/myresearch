<script setup lang="ts">
import { BSIcon } from "cdh-vue-lib";
import { useI18n } from "vue-i18n";

const title = useAppConfig().globalTitle;
const i18n = useI18n();

function setLocale(locale: string) {
    i18n.locale.value = locale;
    localStorage.locale = locale;
}
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
            <div v-if="true" class="border-left px-3">
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
            <!-- TODO: make only relevant link appear, 
            once we can check if user.is_authenticated -->
            <a href="/saml/login/" class="nav-link ms-auto"> Login </a>
            <div class="nav-link">|</div>
            <a href="/saml/logout/" class="nav-link"> Logout </a>
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
