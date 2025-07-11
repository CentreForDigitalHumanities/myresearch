<script setup lang="ts">
import { BSButton } from 'cdh-vue-lib';


</script>

<template>
    <div class="uu-content">
        <Title>{{ $t("MyResearch") }}</Title>
        <div class="uu-hero">
            <h1>{{ $t("Welcome to MyResearch!") }}</h1>
        </div>
        <div class="uu-container">
            <div class="col-12">
                <p>{{ $t("Welcome!") }}</p>
                <BSButton variant="primary"href="/vwr">
                    {{ $t("Go to Processing Registry") }}
                </BSButton>
            </div>
        </div>
    </div>
</template>

<style scoped>

</style>
