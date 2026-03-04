<script lang="ts" setup>
import { useQuery } from "@vue/apollo-composable";
import { BSIcon } from "cdh-vue-lib";
import useStaticFile from "~/composables/useStaticFile";
import { graphql } from "~/generated/gql";
import type { GetFirstSlugQuery } from "~/generated/gql/graphql";

// We only need to know the slug of the top-level form so we can link to it.
const GET_FIRST_SLUG = graphql(`
    query GetFirstSlug {
        form {
            formId
            steps {
                stepId
                slug
            }
        }
    }
`);

const { result } = useQuery<GetFirstSlugQuery>(GET_FIRST_SLUG);
const slug = computed<string | null>(() => {
    const firstStep = result.value?.form?.steps[0];
    return firstStep?.slug || null;
});
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
                        <NuxtLink to="/studies/" class="nav-link" active-class="active">
                            {{ $t("Studies") }}
                        </NuxtLink>
                    </li>
                    <li>
                        <NuxtLink
                            v-if="slug"
                            :to="{
                                name: 'procreg-slug',
                                params: { slug },
                            }"
                            class="nav-link"
                            active-class="active"
                        >
                            {{ $t("Processing Registry") }}
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

<style scoped lang="scss">
@use "node_modules/uu-bootstrap/scss/configuration";

.year-select {
    .dropdown-item {
        display: flex;
        align-items: center;
        line-height: 2rem;
    }
    .year-color-box {
        width: 1.5rem;
        height: 1.5rem;
        display: inline-block;
        margin-right: 0.5rem;

        @each $name, $color in configuration.$theme-colors {
            &.bg-#{$name} {
                background: $color;
            }
        }
    }
}
</style>
