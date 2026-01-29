<script setup lang="ts">
import Notifications from "../components/layout/Notifications/index.vue";
const title = useAppConfig().globalTitle;
</script>

<template>
    <div class="uu-root-container">
        <Notifications />
        <Head>
            <Title>{{ title }}</Title>
        </Head>
        <LayoutPageHeader />
        <LayoutNavBar />
        <slot />
        <LayoutPageFooter />
    </div>
</template>

<style scoped></style>
