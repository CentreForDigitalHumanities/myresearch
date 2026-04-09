import { useNotificationStore } from "~/stores/notification";

const DEFAULT_NOTIFICATION_TIMEOUT_SECONDS = 8;

/**
 * Creates a notification with the given message, color, and timeout.
 *
 * @param message The message to display in the notification.
 * @param color The color of the notification (info, success, warning, or danger).
 * @param timeout The duration of the notification in seconds.
 */
function useNotification(
  message: string,
  color: NotificationColor = "info",
  timeout: number = DEFAULT_NOTIFICATION_TIMEOUT_SECONDS,
) {
  const notificationStore = useNotificationStore();

  const timeoutMilis = timeout * 1000;
  const timeoutDate = new Date(new Date().getTime() + timeoutMilis);

  notificationStore.create({
    bodyText: message,
    timeout: timeoutDate,
    color,
  });
}

export { useNotification };
