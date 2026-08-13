import { library, config } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

import { faGear, faHouse } from "@fortawesome/free-solid-svg-icons";

config.autoAddCss = false;

library.add(faGear, faHouse);

export default defineNuxtPlugin((nuxtApp) => {
    nuxtApp.vueApp.component("FontAwesomeIcon", FontAwesomeIcon);
});
