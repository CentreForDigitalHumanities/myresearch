import {
    Alert,
    Button,
    Collapse,
    Dropdown,
    Modal,
    Offcanvas,
    Popover,
    ScrollSpy,
    Tab,
    Toast,
    Tooltip,
} from "bootstrap";

export default defineNuxtPlugin(() => {
    return {
        provide: {
            bootstrap: {
                Alert,
                Button,
                Collapse,
                Dropdown,
                Modal,
                Offcanvas,
                Popover,
                ScrollSpy,
                Tab,
                Toast,
                Tooltip,
            },
        },
    };
});
