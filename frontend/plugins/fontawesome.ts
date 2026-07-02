import { library, config } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

import { faGear, faHouse } from "@fortawesome/free-solid-svg-icons";

config.autoAddCss = false;

library.add(faGear, faHouse);

export default defineNuxtPlugin((nuxtApp) => {
    // @ts-expect-error: "Expression produces a union type that is too complex to represent."
    // This is a bug related to FontAwesomeIcon in combination with TS; not ours to fix.
    nuxtApp.vueApp.component("FontAwesomeIcon", FontAwesomeIcon);
});
