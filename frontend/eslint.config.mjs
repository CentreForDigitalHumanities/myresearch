import globals from "globals";
import pluginJs from "@eslint/js";
import tseslint from "typescript-eslint";
import pluginVue from "eslint-plugin-vue";
import prettier from "eslint-plugin-prettier/recommended";
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
      "vue/multi-word-component-names": [
        "warn",
        {
          // Allow single-word component names in Nuxt file names and
          // parametrized pages.
          ignores: ["index", "default", "error", "slug"],
        },
      ],
      "vue/no-unused-vars": "warn",
    },
  },
  {
    ignores: ["node_modules", ".nuxt", ".output", "dist"],
  },
  // prettier
  prettier,
  {
    rules: {
      ...prettier.rules,
      "prettier/prettier": [
        "warn",
        {
          endOfLine: "lf", // Warn on CRLF line endings
          tabWidth: 4, // Use 4 spaces for indentation
        },
      ],
    },
  },
]);
