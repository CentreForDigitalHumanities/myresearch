<script lang="ts" setup>
import { computed } from "vue";
import { Notification, useNotificationStore } from "~/stores/notification";
import { useDayJS } from "#imports";

// This component has (mostly) been copied from DIAPP!
// See: https://github.com/CentreForDigitalHumanities/DIAPP

const props = defineProps<{
    notification: Notification;
}>();

const containerClasses = computed(() => {
    let classes = "toast show ";

    if (!props.notification.headerText) {
        if (props.notification.color) {
            classes += `text-bg-${props.notification.color} `;
        } else {
            classes += "text-bg-primary ";
        }
    }

    return classes;
});

const headerClasses = computed(() => {
    let classes = "toast-header ";

    if (props.notification.color) {
        classes += `text-bg-${props.notification.color} `;
    } else {
        classes += "text-bg-primary ";
    }

    return classes;
});

const timeoutSeconds = computed(() => {
    return useDayJS(props.notification.timeout).diff(
        useDayJS(props.notification.creation),
        "s"
    );
});

const timeoutElapsed = computed(() => {
    return (
        timeoutSeconds.value -
        useDayJS(props.notification.timeout).diff(useDayJS(), "s") -
        1
    );
});

const timeoutStyles = computed(() => {
    return `--seconds: ${timeoutSeconds.value};--elapsed: ${timeoutElapsed.value}`;
});

function dismiss() {
    if (!props.notification.dismissible) {
        return;
    }

    useNotificationStore().dismiss(props.notification.id);
}
</script>

<template>
    <div
        :id="notification.id"
        :class="containerClasses"
        role="alert"
        aria-live="assertive"
        aria-atomic="true"
    >
        <div v-if="notification.headerText" :class="headerClasses">
            <div class="me-auto fw-bolder">
                {{ notification.headerText }}
            </div>
            <button
                v-if="notification.dismissible"
                type="button"
                class="btn-close"
                aria-label="Close"
                @click="dismiss"
            />
        </div>
        <div v-if="notification.headerText" class="toast-body">
            {{ notification.bodyText }}
        </div>
        <div
            v-else
            class="toast-body fw-bold d-flex justify-content-between align-items-start"
        >
            <div>
                {{ notification.bodyText }}
            </div>

            <button
                v-if="notification.dismissible"
                type="button"
                class="btn-close"
                aria-label="Close"
                @click="dismiss"
            />
        </div>
        <div
            v-if="notification.timeout"
            class="toast-timeout"
            :style="timeoutStyles"
        />
    </div>
</template>
