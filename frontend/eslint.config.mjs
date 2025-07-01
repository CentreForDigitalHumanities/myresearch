import globals from "globals";
import pluginJs from "@eslint/js";
import tseslint from "typescript-eslint";
import pluginVue from "eslint-plugin-vue";
import prettier from "eslint-plugin-prettier/recommended";
import vueConfigTypescript, {
  defineConfigWithVueTs,
} from "@vue/eslint-config-typescript";
import vueConfigPrettier from "@vue/eslint-config-prettier";

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
    },
  },
  // ts
  ...tseslint.configs.recommended,
  ...tseslint.configs['strictTypeChecked'],
  {
    rules: {
      "@typescript-eslint/no-unused-vars": "warn",
      "@typescript-eslint/no-explicit-any": "error",
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
  },
  {
    ignores: ["node_modules", ".nuxt", ".output", "dist"],
  },
  // prettier
  prettier,
]);
