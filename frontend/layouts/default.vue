<script setup lang="ts">
const title = useAppConfig().globalTitle;
</script>

<template>
    <div class="uu-root-container">
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
