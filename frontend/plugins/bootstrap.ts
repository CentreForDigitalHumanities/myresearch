import { Collapse } from "bootstrap";

export default defineNuxtPlugin(() => {
    return {
        provide: {
            bootstrap: {
                Collapse,
            },
        },
    };
});
