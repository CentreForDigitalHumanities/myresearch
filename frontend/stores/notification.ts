import { defineStore, acceptHMRUpdate } from "pinia";
import { v4 as uuidv4 } from "uuid";
import _ from "lodash";
import { useDayJS } from "#imports";

// This store has (mostly) been copied from DIAPP!
// See: https://github.com/CentreForDigitalHumanities/DIAPP

class Notification {
    id: string;
    headerText?: string;
    bodyText?: string;
    creation: Date | string;
    timeout?: Date;
    color?: string;
    dismissible: boolean;

    constructor(data: Partial<Notification>) {
        this.id = data.id || uuidv4();
        this.dismissible = data.dismissible || true;
        this.creation = data.creation || new Date();
        this.timeout = data.timeout;

        this.headerText = data.headerText;
        this.bodyText = data.bodyText;
        this.color = data.color;
    }
}

interface State {
    data: Notification[];
    loaded: boolean; // Not used, but required for the serializers
}

const useNotificationStore = defineStore("notification", {
    state: (): State => ({
        data: [],
        loaded: false,
    }),
    getters: {
        notifications(): Notification[] {
            _.remove(this.data, (notification) => {
                if (notification.timeout) {
                    // Remove if notification timeout is in the past
                    return useDayJS(notification.timeout).isBefore(useDayJS());
                }

                return false;
            });

            return this.data;
        },
    },
    actions: {
        getIndexById(id: string) {
            return this.data.findIndex((item) => item.id === id);
        },
        create(data: Partial<Notification>) {
            const notification = new Notification(data);
            this.data.push(notification);

            if (data.timeout) {
                setTimeout(
                    () => this.dismiss(notification.id),
                    useDayJS(notification.timeout).diff(useDayJS(), "ms")
                );
            }

            return notification;
        },
        dismiss(notification: string | Notification) {
            if (typeof notification === "object") {
                notification = notification.id;
            }

            _.remove(this.data, (n) => {
                return n.id === notification;
            });
        },
    },
});

// For hot reloading during dev
if (import.meta.hot) {
    import.meta.hot.accept(
        // eslint-disable-next-line @typescript-eslint/ban-ts-comment
        // @ts-ignore
        acceptHMRUpdate(useNotificationStore, import.meta.hot),
    );
}

export { useNotificationStore, Notification };
