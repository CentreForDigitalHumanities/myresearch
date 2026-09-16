import { defineVitestConfig } from "@nuxt/test-utils/config";
import path from "path";

export default defineVitestConfig({
    test: {
        environment: "nuxt",
        // Needed because Nuxt takes a while to start up.
        hookTimeout: 60000,
        setupFiles: ["./vitest.setup.ts"],
    },
    resolve: {
        alias: {
            "~": path.resolve(import.meta.dirname, "./"),
            "@": path.resolve(import.meta.dirname, "./"),
        },
    },
});
