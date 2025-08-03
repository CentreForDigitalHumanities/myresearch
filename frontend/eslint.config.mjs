import globals from "globals";
import pluginJs from "@eslint/js";
import tseslint from "typescript-eslint";
import pluginVue from "eslint-plugin-vue";
import { defineConfigWithVueTs } from "@vue/eslint-config-typescript";

export default defineConfigWithVueTs([
    {
        languageOptions: {
            globals: {
                ...globals.browser,
                ...globals.node,
            },
        },
    },
    // js
    pluginJs.configs.recommended,
    {
        rules: {
            "no-unused-vars": "warn",
            // TypeScript already handles this, and ESLint does not know about
            // built-in / globally defined variables.
            "no-undef": "off",
        },
    },
    // ts
    ...tseslint.configs.recommended,
    ...tseslint.configs["strictTypeChecked"],
    {
        languageOptions: {
            parserOptions: {
                projectService: true,
                tsconfigRootDir: import.meta.dirname,
            },
        },
        rules: {
            "@typescript-eslint/no-unused-vars": "warn",
            "@typescript-eslint/no-explicit-any": "error",
            "@typescript-eslint/no-unnecessary-type-parameters": "warn",
        },
    },
    // vue
    ...pluginVue.configs["flat/essential"],
    ...pluginVue.configs["flat/strongly-recommended"],
    ...pluginVue.configs["flat/recommended"],
    {
        files: ["*.vue", "**/*.vue"],
        languageOptions: {
            parserOptions: {
                ecmaVersion: "latest",
                sourceType: "module",
                parser: tseslint.parser,
                extraFileExtensions: [".vue"],
            },
        },
        rules: {
            // Set indent to 4 spaces for HTML in .vue files.
            "vue/html-indent": ["warn", 4],
            // Allow more than one attribute per line in Vue templates.
            "vue/max-attributes-per-line": "off",
            // Allow single-word component names in Nuxt file names.
            "vue/multi-word-component-names": [
                "warn",
                {
                    ignores: ["index", "default", "error"],
                },
            ],
            "vue/no-unused-vars": "warn",
        },
    },
    {
        ignores: ["node_modules", ".nuxt", ".output", "dist", "generated"],
    },
]);
