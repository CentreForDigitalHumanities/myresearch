import { defineStore } from "pinia";
import { v4 as uuidv4 } from "uuid";

type NotificationInput = Pick<
    Notification,
    "bodyText" | "timeout" | "color" | "dismissible" | "headerText"
>;

export type NotificationColor = "info" | "success" | "warning" | "danger";

export class Notification {
    id: string;
    bodyText: string;
    timeout: Date;
    color: NotificationColor;
    creation: Date | string;
    dismissible?: boolean;
    headerText?: string;

    constructor(data: NotificationInput) {
        this.id = uuidv4();
        this.dismissible = data.dismissible || true;
        this.creation = new Date();
        this.timeout = data.timeout;
        this.headerText = data.headerText;
        this.bodyText = data.bodyText;
        this.color = data.color;
    }
}

export const useNotificationStore = defineStore("notification", () => {
    const notificationList = ref<Notification[]>([]);

    // Getter for notifications.
    // Removes expired notifications as a side effect.
    const notifications = computed(() => {
        removeExpired();
        return notificationList.value;
    });

    function create(data: NotificationInput): void {
        const notification = new Notification(data);
        notificationList.value.push(notification);

        setTimeout(() => {
            dismiss(notification);
        }, notification.timeout.getTime() - new Date().getTime());
    }

    function dismiss(notification: string | Notification): void {
        if (typeof notification !== "string") {
            notification = notification.id;
        }

        const newNotifications = notificationList.value.filter(
            (n) => n.id !== notification,
        );
        notificationList.value = newNotifications;
    }

    function removeExpired(): void {
        const now = new Date();
        const newNotifications = notificationList.value.filter(
            (n) => n.timeout > now,
        );

        notificationList.value = newNotifications;
    }

    function clear(): void {
        notificationList.value = [];
    }

    return {
        notifications,
        create,
        dismiss,
        clear,
    };
});
