<script setup lang="ts">
import NotificationContainer from "~/components/layout/notifications/NotificationContainer.vue";

const title = useAppConfig().globalTitle;
</script>

<template>
  <div class="uu-root-container">
    <NotificationContainer />
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
