<script lang="ts" setup>
import { useNotificationStore } from "~/stores/notification";

const notificationStore = useNotificationStore();

// This component has (mostly) been copied from DIAPP!
// See: https://github.com/CentreForDigitalHumanities/DIAPP
</script>

<template>
    <Teleport to="body">
        <div class="toast-container position-fixed bottom-0 end-0 me-3 mb-3">
            <LayoutNotificationsItem
                v-for="notification in notificationStore.notifications"
                :key="notification.id"
                :notification="notification"
            />
        </div>
    </Teleport>
</template>
