<script setup lang="ts">
import { BSIcon } from "cdh-vue-lib";
const title = useAppConfig().globalTitle;
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
                v-if="true"
                class="border-left px-3"
            >
                <NuxtLink to="/admin/" class="nav-link">
                    <BSIcon icon="gear" size="lg" />
                </NuxtLink>
            </div>
            <div
                v-if="false"
                class="language-switcher"
            >
                English
            </div>
            <div
                v-if="true"
                class="language-switcher"
            >
                Dutch
            </div>
        </div>
        <div class="uu-header-row">
            <div class="ms-auto">
                Not logged in
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
