<script setup lang="ts">
import Default from "~/layouts/default.vue";

const error = useError();
</script>

<template>
    <default>
        <div v-if="error" class="uu-content">
            <!-- page not found page -->
            <template v-if="error.statusCode === 404">
                <div class="uu-hero">
                    <h1>404</h1>
                </div>
                <div class="uu-container">
                    <p>404</p>
                </div>
            </template>

            <!-- no permission page -->
            <template v-else-if="error.statusCode === 403">
                <div class="uu-hero">
                    <h1>403</h1>
                </div>
                <div class="uu-container">
                    <p>403</p>
                </div>
            </template>

            <!-- catch all for all other errors -->
            <template v-else>
                <div class="uu-hero">
                    <h1>Error</h1>
                </div>
                <div class="uu-container">
                    <p>Error</p>
                </div>
            </template>
        </div>
    </default>
</template>
