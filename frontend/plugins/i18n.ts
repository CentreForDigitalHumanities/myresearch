import { createI18n } from "vue-i18n";
import nl from "../locales/nl.json";

const messages = {
    nl,
};
const defaultLocale = "en";

/* Get locale from local storage or, if not available, from the browser
   data, ignoring the country part (i.e. nl-NL becomes nl).
 */
const locale =
    localStorage.getItem("locale") ||
    navigator.language.split("-")[0] ||
    defaultLocale;

export const i18n = createI18n({
    // Use the newer Composition API
    legacy: false,
    globalInjection: true,
    locale,
    messages,
    fallbackFormat: true,
    fallbackLocale: defaultLocale,
    fallbackWarn: false,
    missingWarn: false,
});

export default defineNuxtPlugin(({ vueApp }) => {
    vueApp.use(i18n);
});
