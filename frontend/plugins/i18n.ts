import {createI18n} from "vue-i18n";
import nl from "../locales/nl.json";

const messages = {
    nl
};
const defaultLocale = "en";

/* Get locale from local storage or, if not available, from the browser
   data, ignoring the country part (i.e. nl-NL becomes nl).
 */
let locale: string = localStorage.locale ?? navigator.language.split("-")[0];
if (!(locale in messages)) {
    locale = "en";
}

export const i18n = createI18n({
    globalInjection: true,
    locale,
    messages,
    formatFallbackMessages: true,
    fallbackLocale: defaultLocale,
});

export default defineNuxtPlugin(({ vueApp}) => {
    vueApp.use(i18n);
});
