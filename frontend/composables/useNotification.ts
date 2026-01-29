import { useNotificationStore } from "~/stores/notification";

/**
 * Creates a notification with the given message, color, and timeout.
 * @param message The message to display in the notification.
 * @param color The color of the notification (info, success, warning, or danger).
 * @param timeout The duration of the notification in seconds.
 */
function useNotification(
    message: string,
    color: "info" | "success" | "warning" | "danger" = "info",
    timeout: number = 5
) {
    const notificationStore = useNotificationStore();

    notificationStore.create({
        bodyText: message,
        timeout: useDayJS().add(timeout, "s").toDate(),
        color,
    });
}

export { useNotification };
