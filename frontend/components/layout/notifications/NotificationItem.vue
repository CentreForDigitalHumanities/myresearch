<script lang="ts" setup>
import { useNotificationStore, type Notification } from "~/stores/notification";
import { BSIcon } from "cdh-vue-lib";
import { type NotificationColor } from "~/stores/notification";
import {
    faCircleCheck,
    faCircleExclamation,
    faCircleQuestion,
    faCircleXmark,
    type IconDefinition,
} from "@fortawesome/free-solid-svg-icons";
import { useI18n } from "vue-i18n";

interface Props {
    notification: Notification;
}

const props = defineProps<Props>();

const notificationStore = useNotificationStore();

const { t } = useI18n();

const ICON_MAP: Record<NotificationColor, IconDefinition> = {
    info: faCircleQuestion,
    success: faCircleCheck,
    warning: faCircleExclamation,
    danger: faCircleXmark,
};

const HEADER_TEXT_MAP: Record<NotificationColor, string> = {
    info: t("Info"),
    success: t("Success"),
    warning: t("Warning"),
    danger: t("Error"),
};

const header = computed(() => {
    return (
        props.notification.headerText ||
        HEADER_TEXT_MAP[props.notification.color]
    );
});

const headerClasses = computed(() => {
    return `toast-header text-bg-${props.notification.color}`;
});

const timeoutSeconds = computed(() => {
    const creationTime = new Date(props.notification.creation).getTime();
    const dismissalTime = new Date(props.notification.timeout).getTime();
    return Math.floor((dismissalTime - creationTime) / 1000);
});

const timeoutElapsed = computed(() => {
    const dismissalTime = new Date(props.notification.timeout).getTime();

    return (
        timeoutSeconds.value -
        Math.floor((dismissalTime - new Date().getTime()) / 1000) -
        1
    );
});

function dismiss(): void {
    if (!props.notification.dismissible) {
        return;
    }
    notificationStore.dismiss(props.notification.id);
}
</script>

<template>
    <div
        :id="notification.id"
        role="alert"
        class="toast show overflow-hidden"
        aria-live="assertive"
        aria-atomic="true"
        data-animation="true"
    >
        <div :class="headerClasses">
            <div class="me-auto fw-bolder d-flex align-items-center gap-2">
                <BSIcon :icon="ICON_MAP[notification.color]" />
                <span>{{ header }}</span>
            </div>
            <button
                v-if="notification.dismissible"
                type="button"
                class="btn-close"
                aria-label="Close"
                @click="dismiss"
            />
        </div>
        <div class="toast-body">
            {{ notification.bodyText }}
        </div>
        <div v-if="notification.timeout" class="toast-timeout" />
    </div>
</template>

<style lang="scss" scoped>
.toast-timeout {
    position: relative;
    width: 100%;
    height: 5px;
    background: rgba(0, 0, 0, 0.1);
    --seconds: v-bind(timeoutSeconds);
    --elapsed: v-bind(timeoutElapsed);

    &::after {
        display: block;
        content: "";
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.2);
        animation: toast-timeout calc(var(--seconds) * 1s) linear;
        animation-iteration-count: 1;
        animation-delay: calc(-1s * var(--elapsed));
    }
}

@keyframes toast-timeout {
    from {
        width: 0;
    }
    to {
        width: 100%;
    }
}
</style>
