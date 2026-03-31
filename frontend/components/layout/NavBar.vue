<script lang="ts" setup>
import { BSIcon } from "cdh-vue-lib";
import useStaticFile from "~/composables/useStaticFile";

const currentUser = computed(() => useCurrentUserStore().currentUser)
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
                        <NuxtLink v-if="currentUser" to="/procreg/start" class="nav-link" active-class="active">{{ $t("New study") }}</NuxtLink>
                    </li>
                    <li v-if="currentUser">
                        <NuxtLink to="/studies/" class="nav-link" active-class="active">
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
