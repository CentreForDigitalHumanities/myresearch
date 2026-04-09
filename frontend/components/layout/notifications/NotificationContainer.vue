<script lang="ts" setup>
import { useNotificationStore } from "~/stores/notification";
import NotificationItem from "./NotificationItem.vue";

const notificationStore = useNotificationStore();
</script>

<template>
  <Teleport to="body">
    <TransitionGroup
      name="toast-list"
      tag="div"
      class="toast-container position-fixed bottom-0 end-0 me-3 mb-3"
    >
      <NotificationItem
        v-for="notification in notificationStore.notifications"
        :key="notification.id"
        :notification="notification"
      />
    </TransitionGroup>
  </Teleport>
</template>

<style lang="scss" scoped>
.toast-list-enter-active,
.toast-list-leave-active {
  transition: all 0.3s ease;
}

.toast-list-enter-from,
.toast-list-leave-to {
  opacity: 0;
}

.toast-list-enter-from {
  transform: translateX(30px);
}

.toast-list-leave-to {
  transform: translateX(-30px);
}
</style>
